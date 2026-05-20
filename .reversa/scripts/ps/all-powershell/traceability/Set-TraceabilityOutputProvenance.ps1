#Requires -Version 5.0

param(
    [string]$TargetFolder,
    [string]$ManifestDefinitionPath,
    [string]$ManifestWrapperPath,
    [ValidateSet('module', 'feature', 'combined', 'unspecified')]
    [string]$BuildMethod = 'unspecified',
    [string]$BuildScope = 'unspecified',
    [string[]]$SourceInputs = @(),
    [string[]]$SupportingSnapshots = @(),
    [string]$WorkingTraceabilitySource,
    [string]$Operator = $env:USERNAME,
    [string]$GeneratedOn,
    [string[]]$ArtifactFiles = @()
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($TargetFolder)) {
    $TargetFolder = $PSScriptRoot
}

$resolvedTargetFolder = [System.IO.Path]::GetFullPath($TargetFolder)
if (-not (Test-Path -LiteralPath $resolvedTargetFolder)) {
    throw "TargetFolder not found: $resolvedTargetFolder"
}

if ([string]::IsNullOrWhiteSpace($GeneratedOn)) {
    $GeneratedOn = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
}

if ([string]::IsNullOrWhiteSpace($WorkingTraceabilitySource)) {
    $WorkingTraceabilitySource = $resolvedTargetFolder
}

function Resolve-DefaultPath {
    param(
        [string]$ExplicitPath,
        [string[]]$CandidatePaths
    )

    if (-not [string]::IsNullOrWhiteSpace($ExplicitPath)) {
        return $ExplicitPath
    }

    foreach ($candidatePath in $CandidatePaths) {
        if (-not [string]::IsNullOrWhiteSpace($candidatePath) -and (Test-Path -LiteralPath $candidatePath)) {
            return $candidatePath
        }
    }

    return ''
}

function Get-XmlValue {
    param(
        [xml]$Xml,
        [string]$XPath
    )

    $node = $Xml.SelectSingleNode($XPath)
    if ($null -eq $node) {
        return ''
    }

    return [string]$node.InnerText
}

function Get-DefaultArtifactFiles {
    return @(
        'field-crosswalk.md',
        'field-crosswalk copy 2.md',
        'master-reports-index.json',
        'master-reports-output-lineage.json',
        'master-reports-output-fields.csv',
        'master-reports-output-fields-by-field.csv',
        'master-reports-build-fields.csv',
        'master-reports-build-fields-by-field.csv',
        'clearinghouse-to-report-lineage.csv',
        'clearinghouse-to-report-lineage.json',
        'lineage-enrichment-summary.md',
        'psis-directory-schema-mapping.csv',
        'psis-directory-schema-mapping.json',
        'PSIS-DIRECTORY-SCHEMA.md',
        'field-to-reports-mapping.csv',
        'field-to-reports-mapping.json',
        'REPORT-INTEGRATION-SUMMARY.md',
        'TRACEABILITY-RERUN-PLAYBOOK.md'
    )
}

function New-ProvenanceObject {
    param(
        [string]$OutputFile,
        [string]$Format,
        [string]$ProvenanceStrategy,
        [string]$ManifestCode,
        [string]$Version,
        [string]$CurrentSchoolYear,
        [string]$StackKey
    )

    return [ordered]@{
        output_file = $OutputFile
        output_format = $Format
        provenance_strategy = $ProvenanceStrategy
        generated_on = $GeneratedOn
        operator = $Operator
        target_folder = $resolvedTargetFolder
        working_traceability_source = $WorkingTraceabilitySource
        manifest_definition_source = $ManifestDefinitionPath
        manifest_wrapper_source = $ManifestWrapperPath
        manifest_code = $ManifestCode
        version = $Version
        current_school_year = $CurrentSchoolYear
        build_method = $BuildMethod
        build_scope = $BuildScope
        stack_key = $StackKey
        declared_source_inputs = @($SourceInputs)
        supporting_snapshots = @($SupportingSnapshots)
    }
}

function Convert-ProvenanceToMarkdown {
    param([hashtable]$Provenance)

    $sourceInputsText = if (@($Provenance.declared_source_inputs).Count -gt 0) {
        @($Provenance.declared_source_inputs | ForEach-Object { "- $_" }) -join [Environment]::NewLine
    }
    else {
        '- None declared'
    }

    $supportingSnapshotsText = if (@($Provenance.supporting_snapshots).Count -gt 0) {
        @($Provenance.supporting_snapshots | ForEach-Object { "- $_" }) -join [Environment]::NewLine
    }
    else {
        '- None declared'
    }

    return @(
        '## Output Provenance',
        '',
        ("- OutputFile: {0}" -f $Provenance.output_file),
        ("- OutputFormat: {0}" -f $Provenance.output_format),
        ("- ProvenanceStrategy: {0}" -f $Provenance.provenance_strategy),
        ("- GeneratedOn: {0}" -f $Provenance.generated_on),
        ("- Operator: {0}" -f $Provenance.operator),
        ("- ManifestCode: {0}" -f $Provenance.manifest_code),
        ("- Version: {0}" -f $Provenance.version),
        ("- CurrentSchoolYear: {0}" -f $Provenance.current_school_year),
        ("- BuildMethod: {0}" -f $Provenance.build_method),
        ("- BuildScope: {0}" -f $Provenance.build_scope),
        ("- StackKey: {0}" -f $Provenance.stack_key),
        '',
        '### Source References',
        '',
        ("- ManifestDefinitionSource: {0}" -f $Provenance.manifest_definition_source),
        ("- ManifestWrapperSource: {0}" -f $Provenance.manifest_wrapper_source),
        ("- WorkingTraceabilitySource: {0}" -f $Provenance.working_traceability_source),
        '',
        '### Declared Additional Source Inputs',
        '',
        $sourceInputsText,
        '',
        '### Declared Supporting Snapshots',
        '',
        $supportingSnapshotsText
    ) -join [Environment]::NewLine
}

function Set-MarkdownProvenance {
    param(
        [string]$FilePath,
        [hashtable]$Provenance
    )

    $startMarker = '<!-- TRACEABILITY_PROVENANCE_START -->'
    $endMarker = '<!-- TRACEABILITY_PROVENANCE_END -->'
    $content = Get-Content -LiteralPath $FilePath -Raw
    $blockBody = Convert-ProvenanceToMarkdown -Provenance $Provenance
    $block = @(
        $startMarker,
        $blockBody,
        $endMarker
    ) -join [Environment]::NewLine

    if ($content.Contains($startMarker) -and $content.Contains($endMarker)) {
        $pattern = '(?s)<!-- TRACEABILITY_PROVENANCE_START -->.*?<!-- TRACEABILITY_PROVENANCE_END -->'
        $updatedContent = [regex]::Replace($content, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block }, 1)
    }
    else {
        $normalizedContent = $content -replace "`r`n", "`n"
        $lines = @($normalizedContent -split "`n")
        $insertIndex = 0
        if ($lines.Count -gt 0 -and $lines[0] -match '^#') {
            $insertIndex = 1
            while ($insertIndex -lt $lines.Count -and ($lines[$insertIndex] -match '^\s*$' -or $lines[$insertIndex] -match '^>')) {
                $insertIndex++
            }
        }

        $before = if ($insertIndex -gt 0) { @($lines[0..($insertIndex - 1)]) } else { @() }
        $after = if ($insertIndex -lt $lines.Count) { @($lines[$insertIndex..($lines.Count - 1)]) } else { @() }
        $updatedLines = @()
        if ($before.Count -gt 0) {
            $updatedLines += $before
        }
        if ($updatedLines.Count -gt 0 -and $updatedLines[-1] -ne '') {
            $updatedLines += ''
        }
        $updatedLines += @($block -split "`n")
        $updatedLines += ''
        if ($after.Count -gt 0) {
            $updatedLines += $after
        }
        $updatedContent = $updatedLines -join [Environment]::NewLine
    }

    Set-Content -LiteralPath $FilePath -Value $updatedContent -Encoding UTF8
}

function Convert-ProvenanceToHtml {
    param([hashtable]$Provenance)

    $sourceInputsHtml = if (@($Provenance.declared_source_inputs).Count -gt 0) {
        @($Provenance.declared_source_inputs | ForEach-Object { "<li>$([System.Net.WebUtility]::HtmlEncode([string]$_))</li>" }) -join ''
    }
    else {
        '<li>None declared</li>'
    }

    $supportingSnapshotsHtml = if (@($Provenance.supporting_snapshots).Count -gt 0) {
        @($Provenance.supporting_snapshots | ForEach-Object { "<li>$([System.Net.WebUtility]::HtmlEncode([string]$_))</li>" }) -join ''
    }
    else {
        '<li>None declared</li>'
    }

    return @(
        '<section class="traceability-provenance" style="border:1px solid #c7d3dd;padding:12px;margin:12px 0;background:#f7fafc;font-family:Segoe UI, Arial, sans-serif;font-size:13px;">',
        '<h2 style="margin-top:0;">Output Provenance</h2>',
        '<ul>',
        ("<li><strong>OutputFile:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.output_file)),
        ("<li><strong>OutputFormat:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.output_format)),
        ("<li><strong>ProvenanceStrategy:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.provenance_strategy)),
        ("<li><strong>GeneratedOn:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.generated_on)),
        ("<li><strong>Operator:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.operator)),
        ("<li><strong>ManifestCode:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.manifest_code)),
        ("<li><strong>Version:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.version)),
        ("<li><strong>CurrentSchoolYear:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.current_school_year)),
        ("<li><strong>BuildMethod:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.build_method)),
        ("<li><strong>BuildScope:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.build_scope)),
        ("<li><strong>StackKey:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.stack_key)),
        '</ul>',
        '<h3>Source References</h3>',
        '<ul>',
        ("<li><strong>ManifestDefinitionSource:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.manifest_definition_source)),
        ("<li><strong>ManifestWrapperSource:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.manifest_wrapper_source)),
        ("<li><strong>WorkingTraceabilitySource:</strong> {0}</li>" -f [System.Net.WebUtility]::HtmlEncode([string]$Provenance.working_traceability_source)),
        '</ul>',
        '<h3>Declared Additional Source Inputs</h3>',
        ("<ul>{0}</ul>" -f $sourceInputsHtml),
        '<h3>Declared Supporting Snapshots</h3>',
        ("<ul>{0}</ul>" -f $supportingSnapshotsHtml),
        '</section>'
    ) -join [Environment]::NewLine
}

function Set-HtmlProvenance {
    param(
        [string]$FilePath,
        [hashtable]$Provenance
    )

    $startMarker = '<!-- TRACEABILITY_PROVENANCE_START -->'
    $endMarker = '<!-- TRACEABILITY_PROVENANCE_END -->'
    $content = Get-Content -LiteralPath $FilePath -Raw
    $blockBody = Convert-ProvenanceToHtml -Provenance $Provenance
    $block = @(
        $startMarker,
        $blockBody,
        $endMarker
    ) -join [Environment]::NewLine

    if ($content.Contains($startMarker) -and $content.Contains($endMarker)) {
        $pattern = '(?s)<!-- TRACEABILITY_PROVENANCE_START -->.*?<!-- TRACEABILITY_PROVENANCE_END -->'
        $updatedContent = [regex]::Replace($content, $pattern, [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $block }, 1)
    }
    elseif ($content -match '(?is)<body[^>]*>') {
        $updatedContent = [regex]::Replace($content, '(?is)(<body[^>]*>)', [System.Text.RegularExpressions.MatchEvaluator]{ param($m) $m.Groups[1].Value + [Environment]::NewLine + $block + [Environment]::NewLine }, 1)
    }
    else {
        $updatedContent = $block + [Environment]::NewLine + $content
    }

    Set-Content -LiteralPath $FilePath -Value $updatedContent -Encoding UTF8
}

function Set-StructuredProvenanceCompanions {
    param(
        [string]$FilePath,
        [hashtable]$Provenance
    )

    $markdownSidecarPath = "$FilePath.provenance.md"
    $jsonSidecarPath = "$FilePath.provenance.json"
    $markdownContent = Convert-ProvenanceToMarkdown -Provenance $Provenance

    Set-Content -LiteralPath $markdownSidecarPath -Value $markdownContent -Encoding UTF8
    $Provenance | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $jsonSidecarPath -Encoding UTF8
}

[string]$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$ManifestDefinitionPath = Resolve-DefaultPath -ExplicitPath $ManifestDefinitionPath -CandidatePaths @(
    (Join-Path $resolvedTargetFolder 'manifest\UTREx_Definition.xml'),
    (Join-Path $resolvedTargetFolder 'UTREx_Definition.xml'),
    (Join-Path $repoRoot 'UTREx_SIF_VRF-develop\UTREx_VRF_ReportCollector\Manifests\UTREx_Definition.xml'),
    (Join-Path $repoRoot 'UTREx_VRF_ReportCollector\Manifests\UTREx_Definition.xml')
)
$ManifestWrapperPath = Resolve-DefaultPath -ExplicitPath $ManifestWrapperPath -CandidatePaths @(
    (Join-Path $resolvedTargetFolder 'manifest\UTREx_Wrapper.xml'),
    (Join-Path $resolvedTargetFolder 'UTREx_Wrapper.xml'),
    (Join-Path $repoRoot 'UTREx_SIF_VRF-develop\UTREx_VRF_ReportCollector\Manifests\UTREx_Wrapper.xml'),
    (Join-Path $repoRoot 'UTREx_VRF_ReportCollector\Manifests\UTREx_Wrapper.xml')
)

[xml]$definitionXml = $null
if (-not [string]::IsNullOrWhiteSpace($ManifestDefinitionPath) -and (Test-Path -LiteralPath $ManifestDefinitionPath)) {
    [xml]$definitionXml = Get-Content -LiteralPath $ManifestDefinitionPath -Raw
}

$manifestCode = if ($null -ne $definitionXml) { Get-XmlValue -Xml $definitionXml -XPath "//Property[@Name='Vrf.Property.ManifestCode']" } else { '' }
$version = if ($null -ne $definitionXml) { Get-XmlValue -Xml $definitionXml -XPath '/VRFReportDefinition/Version' } else { '' }
$currentSchoolYear = if ($null -ne $definitionXml) { Get-XmlValue -Xml $definitionXml -XPath "//Property[@Name='Vrf.Property.CurrentSchoolYear']" } else { '' }
$stackKey = if (-not [string]::IsNullOrWhiteSpace($manifestCode) -and -not [string]::IsNullOrWhiteSpace($version)) { '{0}__v{1}' -f $manifestCode, $version } else { '' }

if ($ArtifactFiles.Count -eq 0) {
    $ArtifactFiles = Get-DefaultArtifactFiles
}

$stampedFiles = New-Object System.Collections.Generic.List[string]
$missingFiles = New-Object System.Collections.Generic.List[string]

foreach ($artifactFile in $ArtifactFiles) {
    $artifactPath = Join-Path $resolvedTargetFolder $artifactFile
    if (-not (Test-Path -LiteralPath $artifactPath)) {
        [void]$missingFiles.Add($artifactFile)
        continue
    }

    $extension = [System.IO.Path]::GetExtension($artifactPath).ToLowerInvariant()
    $provenance = New-ProvenanceObject -OutputFile ([System.IO.Path]::GetFileName($artifactPath)) -Format $extension.TrimStart('.') -ProvenanceStrategy '' -ManifestCode $manifestCode -Version $version -CurrentSchoolYear $currentSchoolYear -StackKey $stackKey

    switch ($extension) {
        '.md' {
            $provenance.provenance_strategy = 'inline-markdown-section'
            Set-MarkdownProvenance -FilePath $artifactPath -Provenance $provenance
            [void]$stampedFiles.Add($artifactFile)
        }
        '.json' {
            $provenance.provenance_strategy = 'adjacent-json-sidecar'
            Set-StructuredProvenanceCompanions -FilePath $artifactPath -Provenance $provenance
            [void]$stampedFiles.Add($artifactFile)
        }
        '.csv' {
            $provenance.provenance_strategy = 'adjacent-csv-sidecar'
            Set-StructuredProvenanceCompanions -FilePath $artifactPath -Provenance $provenance
            [void]$stampedFiles.Add($artifactFile)
        }
        '.html' {
            $provenance.provenance_strategy = 'inline-html-section'
            Set-HtmlProvenance -FilePath $artifactPath -Provenance $provenance
            [void]$stampedFiles.Add($artifactFile)
        }
        default {
            $provenance.provenance_strategy = 'adjacent-sidecar'
            Set-StructuredProvenanceCompanions -FilePath $artifactPath -Provenance $provenance
            [void]$stampedFiles.Add($artifactFile)
        }
    }
}

Write-Host "Provenance stamped in folder: $resolvedTargetFolder" -ForegroundColor Green
Write-Host "Files stamped: $($stampedFiles.Count)" -ForegroundColor Green
if ($missingFiles.Count -gt 0) {
    Write-Host "Optional files not found: $($missingFiles.Count)" -ForegroundColor Yellow
}
