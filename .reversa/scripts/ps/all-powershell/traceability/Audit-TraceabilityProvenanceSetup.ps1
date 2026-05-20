#Requires -Version 5.0

param(
    [string]$TraceabilityFolder,
    [string]$OutputFolder
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($TraceabilityFolder)) {
    $TraceabilityFolder = $PSScriptRoot
}

$resolvedTraceabilityFolder = [System.IO.Path]::GetFullPath($TraceabilityFolder)
if (-not (Test-Path -LiteralPath $resolvedTraceabilityFolder)) {
    throw "Traceability folder not found: $resolvedTraceabilityFolder"
}

if ([string]::IsNullOrWhiteSpace($OutputFolder)) {
    $OutputFolder = Join-Path $resolvedTraceabilityFolder 'audit'
}

$resolvedOutputFolder = [System.IO.Path]::GetFullPath($OutputFolder)
if (-not (Test-Path -LiteralPath $resolvedOutputFolder)) {
    $null = New-Item -ItemType Directory -Path $resolvedOutputFolder -Force
}

function Test-InlineProvenanceMarker {
    param([string]$FilePath)

    $content = Get-Content -LiteralPath $FilePath -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($content)) {
        return $false
    }

    return $content.Contains('<!-- TRACEABILITY_PROVENANCE_START -->') -and $content.Contains('<!-- TRACEABILITY_PROVENANCE_END -->')
}

function Test-IsUnderPath {
    param(
        [string]$CandidatePath,
        [string]$RootPath
    )

    $normalizedCandidate = [System.IO.Path]::GetFullPath($CandidatePath).TrimEnd('\')
    $normalizedRoot = [System.IO.Path]::GetFullPath($RootPath).TrimEnd('\')

    return $normalizedCandidate.StartsWith($normalizedRoot, [System.StringComparison]::OrdinalIgnoreCase)
}

$coreComponents = @(
    [pscustomobject]@{ Name = 'Set-TraceabilityOutputProvenance.ps1'; Type = 'script'; Purpose = 'Per-output provenance stamping helper' },
    [pscustomobject]@{ Name = 'Invoke-TraceabilityOutputStamp.ps1'; Type = 'script'; Purpose = 'Shared post-write stamping invoker' },
    [pscustomobject]@{ Name = 'New-TraceabilitySnapshot.ps1'; Type = 'script'; Purpose = 'Copy-only snapshot helper' },
    [pscustomobject]@{ Name = 'Build-TraceabilityVersionsIndex.ps1'; Type = 'script'; Purpose = 'Versions inventory builder' },
    [pscustomobject]@{ Name = 'Compare-TraceabilitySnapshots.ps1'; Type = 'script'; Purpose = 'Support/conflict compare helper' },
    [pscustomobject]@{ Name = 'TRACEABILITY-RERUN-PLAYBOOK.md'; Type = 'document'; Purpose = 'Local operating rules and rerun order' }
)

$coreStatus = foreach ($component in $coreComponents) {
    $componentPath = Join-Path $resolvedTraceabilityFolder $component.Name
    [pscustomobject]@{
        name = $component.Name
        type = $component.Type
        purpose = $component.Purpose
        exists = Test-Path -LiteralPath $componentPath
        path = $componentPath
    }
}

$infrastructureScripts = @(
    'Set-TraceabilityOutputProvenance.ps1',
    'Invoke-TraceabilityOutputStamp.ps1',
    'New-TraceabilitySnapshot.ps1',
    'Build-TraceabilityVersionsIndex.ps1',
    'Compare-TraceabilitySnapshots.ps1',
    'Audit-TraceabilityProvenanceSetup.ps1'
)

$writePattern = '(?im)\b(Set-Content|Add-Content|Out-File|Export-Csv|Copy-Item)\b'
$stampPattern = 'Invoke-TraceabilityOutputStamp\.ps1|Set-TraceabilityOutputProvenance\.ps1'

$generatorScripts = foreach ($scriptFile in Get-ChildItem -LiteralPath $resolvedTraceabilityFolder -Filter '*.ps1' -File | Sort-Object Name) {
    $content = Get-Content -LiteralPath $scriptFile.FullName -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($content)) {
        continue
    }

    $writeMatches = [regex]::Matches($content, $writePattern)
    if ($writeMatches.Count -eq 0) {
        continue
    }

    $writeOperations = @($writeMatches | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $isInfrastructure = $scriptFile.Name -in $infrastructureScripts
    $hasStampCall = [regex]::IsMatch($content, $stampPattern)

    [pscustomobject]@{
        name = $scriptFile.Name
        path = $scriptFile.FullName
        is_infrastructure = $isInfrastructure
        has_write_operations = $true
        write_operations = $writeOperations
        has_stamp_call = $hasStampCall
        needs_wiring = (-not $isInfrastructure) -and (-not $hasStampCall)
    }
}

$outputExtensions = @('.md', '.csv', '.json', '.html', '.txt')
$outputFiles = foreach ($file in Get-ChildItem -LiteralPath $resolvedTraceabilityFolder -Recurse -File | Sort-Object FullName) {
    if (Test-IsUnderPath -CandidatePath $file.FullName -RootPath $resolvedOutputFolder) {
        continue
    }

    if ($file.Extension.ToLowerInvariant() -notin $outputExtensions) {
        continue
    }

    if ($file.Name -like '*.provenance.*') {
        continue
    }

    if ($file.Name -like '*.backup.*') {
        continue
    }

    $relativePath = $file.FullName.Substring($resolvedTraceabilityFolder.Length).TrimStart('\')
    $extension = $file.Extension.ToLowerInvariant()
    $hasInlineProvenance = $false
    $hasMarkdownSidecar = $false
    $hasJsonSidecar = $false
    $status = 'not-applicable'

    if ($extension -in @('.md', '.html')) {
        $hasInlineProvenance = Test-InlineProvenanceMarker -FilePath $file.FullName
        $status = if ($hasInlineProvenance) { 'ok-inline' } else { 'missing-inline' }
    }
    else {
        $markdownSidecarPath = $file.FullName + '.provenance.md'
        $jsonSidecarPath = $file.FullName + '.provenance.json'
        $hasMarkdownSidecar = Test-Path -LiteralPath $markdownSidecarPath
        $hasJsonSidecar = Test-Path -LiteralPath $jsonSidecarPath
        $status = if ($hasMarkdownSidecar -and $hasJsonSidecar) { 'ok-sidecars' } else { 'missing-sidecars' }
    }

    [pscustomobject]@{
        relative_path = $relativePath.Replace('\', '/')
        extension = $extension
        status = $status
        has_inline_provenance = $hasInlineProvenance
        has_markdown_sidecar = $hasMarkdownSidecar
        has_json_sidecar = $hasJsonSidecar
    }
}

$versionsIndexPath = Join-Path $resolvedTraceabilityFolder 'versions\INDEX.md'
$versionsIndexStatus = [pscustomobject]@{
    exists = Test-Path -LiteralPath $versionsIndexPath
    has_inline_provenance = if (Test-Path -LiteralPath $versionsIndexPath) { Test-InlineProvenanceMarker -FilePath $versionsIndexPath } else { $false }
    path = $versionsIndexPath
}

$missingCore = @($coreStatus | Where-Object { -not $_.exists })
$unwiredGenerators = @($generatorScripts | Where-Object { $_.needs_wiring })
$outputsMissingProvenance = @($outputFiles | Where-Object { $_.status -in @('missing-inline', 'missing-sidecars') })
$wiredGenerators = @($generatorScripts | Where-Object { (-not $_.is_infrastructure) -and $_.has_stamp_call })

$requiredActions = New-Object System.Collections.Generic.List[string]
foreach ($component in $missingCore) {
    [void]$requiredActions.Add("Add missing core component: $($component.name)")
}
foreach ($script in $unwiredGenerators) {
    [void]$requiredActions.Add("Wire generator script to Invoke-TraceabilityOutputStamp.ps1: $($script.name)")
}
foreach ($output in $outputsMissingProvenance) {
    [void]$requiredActions.Add("Regenerate or stamp output with missing provenance: $($output.relative_path)")
}
if ($versionsIndexStatus.exists -and -not $versionsIndexStatus.has_inline_provenance) {
    [void]$requiredActions.Add('Regenerate versions/INDEX.md so it carries inline provenance.')
}
if ($requiredActions.Count -eq 0) {
    [void]$requiredActions.Add('No blocking provenance gaps detected in this traceability folder.')
}

$auditObject = [ordered]@{
    generated_on = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
    traceability_folder = $resolvedTraceabilityFolder
    output_folder = $resolvedOutputFolder
    core_components = @($coreStatus)
    generator_scripts = @($generatorScripts)
    versions_index = $versionsIndexStatus
    output_files = @($outputFiles)
    summary = [ordered]@{
        missing_core_count = $missingCore.Count
        generator_script_count = $generatorScripts.Count
        wired_generator_count = $wiredGenerators.Count
        unwired_generator_count = $unwiredGenerators.Count
        outputs_audited = $outputFiles.Count
        outputs_missing_provenance_count = $outputsMissingProvenance.Count
    }
    required_actions = @($requiredActions)
}

$reportBaseName = 'traceability-provenance-audit'
$jsonPath = Join-Path $resolvedOutputFolder ($reportBaseName + '.json')
$markdownPath = Join-Path $resolvedOutputFolder ($reportBaseName + '.md')

$auditObject | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

$lines = New-Object System.Collections.Generic.List[string]
[void]$lines.Add('# Traceability Provenance Audit')
[void]$lines.Add('')
[void]$lines.Add(('- GeneratedOn: {0}' -f $auditObject.generated_on))
[void]$lines.Add(('- TraceabilityFolder: {0}' -f $auditObject.traceability_folder))
[void]$lines.Add(('- OutputFolder: {0}' -f $auditObject.output_folder))
[void]$lines.Add('')
[void]$lines.Add('## Summary')
[void]$lines.Add('')
[void]$lines.Add(('- MissingCoreComponents: {0}' -f $auditObject.summary.missing_core_count))
[void]$lines.Add(('- GeneratorScriptsAudited: {0}' -f $auditObject.summary.generator_script_count))
[void]$lines.Add(('- WiredGeneratorScripts: {0}' -f $auditObject.summary.wired_generator_count))
[void]$lines.Add(('- UnwiredGeneratorScripts: {0}' -f $auditObject.summary.unwired_generator_count))
[void]$lines.Add(('- OutputsAudited: {0}' -f $auditObject.summary.outputs_audited))
[void]$lines.Add(('- OutputsMissingProvenance: {0}' -f $auditObject.summary.outputs_missing_provenance_count))
[void]$lines.Add('')
[void]$lines.Add('## Core Components')
[void]$lines.Add('')
[void]$lines.Add('| Name | Type | Exists | Purpose |')
[void]$lines.Add('|---|---|---|---|')
foreach ($component in $coreStatus) {
    [void]$lines.Add(("| {0} | {1} | {2} | {3} |" -f $component.name, $component.type, $component.exists, $component.purpose))
}
[void]$lines.Add('')
[void]$lines.Add('## Generator Wiring')
[void]$lines.Add('')
[void]$lines.Add('| Script | Infrastructure | StampCall | WriteOperations | NeedsWiring |')
[void]$lines.Add('|---|---|---|---|---|')
foreach ($script in $generatorScripts) {
    [void]$lines.Add(("| {0} | {1} | {2} | {3} | {4} |" -f $script.name, $script.is_infrastructure, $script.has_stamp_call, ($script.write_operations -join ', '), $script.needs_wiring))
}
[void]$lines.Add('')
[void]$lines.Add('## Versions Index')
[void]$lines.Add('')
[void]$lines.Add(("- Exists: {0}" -f $versionsIndexStatus.exists))
[void]$lines.Add(("- HasInlineProvenance: {0}" -f $versionsIndexStatus.has_inline_provenance))
[void]$lines.Add(("- Path: {0}" -f $versionsIndexStatus.path))
[void]$lines.Add('')
[void]$lines.Add('## Outputs Missing Provenance')
[void]$lines.Add('')
if ($outputsMissingProvenance.Count -eq 0) {
    [void]$lines.Add('- None detected')
}
else {
    foreach ($output in $outputsMissingProvenance) {
        [void]$lines.Add(("- {0} [{1}]" -f $output.relative_path, $output.status))
    }
}
[void]$lines.Add('')
[void]$lines.Add('## Required Actions')
[void]$lines.Add('')
foreach ($action in $requiredActions) {
    [void]$lines.Add(("- {0}" -f $action))
}

Set-Content -LiteralPath $markdownPath -Value ($lines -join [Environment]::NewLine) -Encoding UTF8

Write-Host "Audit markdown: $markdownPath" -ForegroundColor Green
Write-Host "Audit json: $jsonPath" -ForegroundColor Green
Write-Host "Missing core components: $($missingCore.Count)" -ForegroundColor Yellow
Write-Host "Unwired generator scripts: $($unwiredGenerators.Count)" -ForegroundColor Yellow
Write-Host "Outputs missing provenance: $($outputsMissingProvenance.Count)" -ForegroundColor Yellow
