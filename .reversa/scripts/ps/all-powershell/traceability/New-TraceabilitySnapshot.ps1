#Requires -Version 5.0

param(
    [string]$TracingFolder,
    [string]$ManifestDefinitionPath,
    [string]$ManifestWrapperPath,
    [string]$SnapshotRoot,
    [ValidateSet('module', 'feature', 'combined', 'unspecified')]
    [string]$BuildMethod = 'unspecified',
    [string]$BuildScope = '',
    [string[]]$SourceInputs = @(),
    [string[]]$SupportingSnapshots = @(),
    [string]$Operator = $env:USERNAME,
    [string]$ChangeSummary = "",
    [string]$BootstrapNote = "",
    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($TracingFolder)) {
    $TracingFolder = $PSScriptRoot
}

$repoRoot = Split-Path -Parent (Split-Path -Parent $TracingFolder)

if ([string]::IsNullOrWhiteSpace($ManifestDefinitionPath)) {
    $ManifestDefinitionPath = Join-Path $repoRoot 'UTREx_SIF_VRF-develop\UTREx_VRF_ReportCollector\Manifests\UTREx_Definition.xml'
}

if ([string]::IsNullOrWhiteSpace($ManifestWrapperPath)) {
    $ManifestWrapperPath = Join-Path $repoRoot 'UTREx_SIF_VRF-develop\UTREx_VRF_ReportCollector\Manifests\UTREx_Wrapper.xml'
}

if ([string]::IsNullOrWhiteSpace($SnapshotRoot)) {
    $SnapshotRoot = Join-Path $TracingFolder 'versions'
}

$resolvedTracingFolder = [System.IO.Path]::GetFullPath($TracingFolder)
$resolvedSnapshotRoot = [System.IO.Path]::GetFullPath($SnapshotRoot)

if ($resolvedTracingFolder -eq $resolvedSnapshotRoot) {
    throw 'SnapshotRoot cannot be the live working traceability folder. Use a child versions folder instead.'
}

if ($resolvedTracingFolder -eq [System.IO.Path]::GetFullPath((Join-Path $SnapshotRoot $null))) {
    throw 'SnapshotRoot resolution collided with the live working traceability folder.'
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

function New-DirectoryIfMissing {
    param(
        [string]$Path
    )

    if (-not (Test-Path -LiteralPath $Path)) {
        $null = New-Item -ItemType Directory -Path $Path -Force
    }
}

$requiredPaths = @($TracingFolder, $ManifestDefinitionPath, $ManifestWrapperPath)
foreach ($requiredPath in $requiredPaths) {
    if (-not (Test-Path -LiteralPath $requiredPath)) {
        throw "Required path not found: $requiredPath"
    }
}

[xml]$definitionXml = Get-Content -LiteralPath $ManifestDefinitionPath -Raw

$manifestCode = Get-XmlValue -Xml $definitionXml -XPath "//Property[@Name='Vrf.Property.ManifestCode']"
$version = Get-XmlValue -Xml $definitionXml -XPath '/VRFReportDefinition/Version'
$currentSchoolYear = Get-XmlValue -Xml $definitionXml -XPath "//Property[@Name='Vrf.Property.CurrentSchoolYear']"

if ([string]::IsNullOrWhiteSpace($manifestCode)) {
    throw 'ManifestCode was not found in the manifest definition.'
}

if ([string]::IsNullOrWhiteSpace($version)) {
    throw 'Version was not found in the manifest definition.'
}

$snapshotName = '{0}__v{1}' -f $manifestCode, $version
$methodRoot = Join-Path $SnapshotRoot $BuildMethod
$snapshotPath = Join-Path $methodRoot $snapshotName
$manifestSnapshotPath = Join-Path $snapshotPath 'manifest'
$stackKey = '{0}__v{1}' -f $manifestCode, $version

$artifactFiles = @(
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

if ((Test-Path -LiteralPath $snapshotPath) -and -not $Force) {
    throw "Snapshot already exists: $snapshotPath. Use -Force only to refresh the copied snapshot files under versions/."
}

New-DirectoryIfMissing -Path $SnapshotRoot
New-DirectoryIfMissing -Path $methodRoot
New-DirectoryIfMissing -Path $snapshotPath
New-DirectoryIfMissing -Path $manifestSnapshotPath

$copiedArtifacts = New-Object System.Collections.Generic.List[string]
$missingArtifacts = New-Object System.Collections.Generic.List[string]

foreach ($artifactFile in $artifactFiles) {
    $sourcePath = Join-Path $TracingFolder $artifactFile
    if (Test-Path -LiteralPath $sourcePath) {
        Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $snapshotPath $artifactFile) -Force
        [void]$copiedArtifacts.Add($artifactFile)
    }
    else {
        [void]$missingArtifacts.Add($artifactFile)
    }
}

$definitionSnapshotPath = Join-Path $manifestSnapshotPath 'UTREx_Definition.xml'
$wrapperSnapshotPath = Join-Path $manifestSnapshotPath 'UTREx_Wrapper.xml'

Copy-Item -LiteralPath $ManifestDefinitionPath -Destination $definitionSnapshotPath -Force
Copy-Item -LiteralPath $ManifestWrapperPath -Destination $wrapperSnapshotPath -Force

$copiedOn = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'

if ([string]::IsNullOrWhiteSpace($BuildScope)) {
    $BuildScope = 'unspecified'
}

if ([string]::IsNullOrWhiteSpace($BootstrapNote)) {
    $BootstrapNote = 'Bootstrapped from the current traceability working set. This snapshot preserves the present 14.20 artifact state and should be treated as the baseline until an earlier point-in-time snapshot is reconstructed from historical evidence.'
}

if ([string]::IsNullOrWhiteSpace($ChangeSummary)) {
    $ChangeSummary = 'Initial baseline snapshot created from the current working traceability set.'
}

$runMetadataPath = Join-Path $manifestSnapshotPath 'run-metadata.md'
$runMetadata = @"
# Traceability Snapshot Metadata

- ManifestCode: $manifestCode
- Version: $version
- CurrentSchoolYear: $currentSchoolYear
- BuildMethod: $BuildMethod
- BuildScope: $BuildScope
- StackKey: $stackKey
- ConflictReviewTarget: compare snapshots that share the same StackKey across different BuildMethod values
- SnapshotFolder: $snapshotName
- SnapshotCreatedOn: $copiedOn
- Operator: $Operator
- ManifestDefinitionSource: $ManifestDefinitionPath
- ManifestWrapperSource: $ManifestWrapperPath
- ChangeSummary: $ChangeSummary
- BootstrapNote: $BootstrapNote
- ReportInventoryChanged: Unknown - baseline snapshot
- SchemaMappingChanged: Unknown - baseline snapshot
- CrosswalkStructureChanged: Unknown - baseline snapshot
- WorkingSetMutation: None - this helper reads from the live working set and writes only under versions/

## Copied Artifacts

$(($copiedArtifacts | ForEach-Object { "- $_" }) -join [Environment]::NewLine)

## Missing Optional Artifacts

$(if ($missingArtifacts.Count -gt 0) { ($missingArtifacts | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { '- None' })

## Supporting Snapshots

$(if ($SupportingSnapshots.Count -gt 0) { ($SupportingSnapshots | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { '- None declared' })

## Source Inputs Declared For This Snapshot

$(if ($SourceInputs.Count -gt 0) { ($SourceInputs | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { '- None declared beyond the copied working-set artifacts and manifest files' })

## Notes For Next Increment

- Replace the Unknown change flags after comparing this snapshot to the next manifest increment snapshot.
- Compare field-crosswalk.md, master-reports-index.json, master-reports-output-lineage.json, clearinghouse-to-report-lineage.csv, and lineage-enrichment-summary.md first.
- If the copied snapshot must be refreshed later for the same manifest increment, rerun this script with -Force and record why the snapshot copy was updated. The live working traceability files remain untouched.
"@

Set-Content -LiteralPath $runMetadataPath -Value $runMetadata -Encoding UTF8

$summaryPath = Join-Path $snapshotPath 'README.md'
$summary = @"
# $snapshotName

This folder is the manifest-keyed traceability snapshot for $manifestCode v$version.

The live working traceability set in _reversa_sdd/traceability/ is not modified by this helper. This folder contains copies only.

## Traceability Identity

- BuildMethod: $BuildMethod
- BuildScope: $BuildScope
- StackKey: $stackKey
- ConflictReviewTarget: compare same StackKey across module and feature snapshots

## Contents

- manifest/UTREx_Definition.xml: exact manifest definition used for the snapshot
- manifest/UTREx_Wrapper.xml: wrapper file paired with the definition at snapshot time
- manifest/run-metadata.md: run metadata and change notes
- copied working-set traceability artifacts from _reversa_sdd/traceability/

## Created By

New-TraceabilitySnapshot.ps1 on $copiedOn
"@

Set-Content -LiteralPath $summaryPath -Value $summary -Encoding UTF8

$sourceTraceabilityPath = Join-Path $snapshotPath 'output-traceability.md'
$sourceTraceability = @"
# Output Traceability

This snapshot is intended to coexist with other build methods and remain comparable.

## Snapshot Identity

- BuildMethod: $BuildMethod
- BuildScope: $BuildScope
- ManifestCode: $manifestCode
- Version: $version
- StackKey: $stackKey

## Stacking Rule

- Snapshots stack together when they share the same StackKey and have complementary BuildMethod values.

## Conflict Rule

- Investigate conflicts when snapshots share the same StackKey but disagree on field-crosswalk content, lineage outputs, schema mappings, or declared source inputs.

## Primary Conflict Review Files

- field-crosswalk.md
- master-reports-index.json
- master-reports-output-lineage.json
- clearinghouse-to-report-lineage.csv
- lineage-enrichment-summary.md

## Source References Used For This Output

- Manifest definition source: $ManifestDefinitionPath
- Manifest wrapper source: $ManifestWrapperPath
- Working traceability source folder: $TracingFolder

### Copied Working-Set Artifacts

$(($copiedArtifacts | ForEach-Object { "- $TracingFolder\$_" }) -join [Environment]::NewLine)

### Declared Additional Source Inputs

$(if ($SourceInputs.Count -gt 0) { ($SourceInputs | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { '- None declared' })

### Declared Supporting Snapshots

$(if ($SupportingSnapshots.Count -gt 0) { ($SupportingSnapshots | ForEach-Object { "- $_" }) -join [Environment]::NewLine } else { '- None declared' })
"@

Set-Content -LiteralPath $sourceTraceabilityPath -Value $sourceTraceability -Encoding UTF8

$traceabilityJsonPath = Join-Path $snapshotPath 'output-traceability.json'
$traceabilityJson = [ordered]@{
    build_method = $BuildMethod
    build_scope = $BuildScope
    manifest_code = $manifestCode
    version = $version
    current_school_year = $currentSchoolYear
    stack_key = $stackKey
    conflict_review_target = 'compare snapshots with same stack_key across build methods'
    manifest_definition_source = $ManifestDefinitionPath
    manifest_wrapper_source = $ManifestWrapperPath
    tracing_folder_source = $TracingFolder
    copied_artifacts = @($copiedArtifacts)
    declared_source_inputs = @($SourceInputs)
    supporting_snapshots = @($SupportingSnapshots)
}

$traceabilityJson | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $traceabilityJsonPath -Encoding UTF8

$provenanceHelperPath = Join-Path $PSScriptRoot 'Set-TraceabilityOutputProvenance.ps1'
& $provenanceHelperPath `
    -TargetFolder $snapshotPath `
    -ManifestDefinitionPath $ManifestDefinitionPath `
    -ManifestWrapperPath $ManifestWrapperPath `
    -BuildMethod $BuildMethod `
    -BuildScope $BuildScope `
    -SourceInputs $SourceInputs `
    -SupportingSnapshots $SupportingSnapshots `
    -WorkingTraceabilitySource $TracingFolder `
    -Operator $Operator `
    -GeneratedOn $copiedOn `
    -ArtifactFiles ($copiedArtifacts.ToArray())

Write-Host "Snapshot created: $snapshotPath" -ForegroundColor Green
Write-Host "ManifestCode: $manifestCode" -ForegroundColor Green
Write-Host "Version: $version" -ForegroundColor Green
Write-Host "BuildMethod: $BuildMethod" -ForegroundColor Green
Write-Host "StackKey: $stackKey" -ForegroundColor Green
Write-Host "Artifacts copied: $($copiedArtifacts.Count)" -ForegroundColor Green
if ($missingArtifacts.Count -gt 0) {
    Write-Host "Optional artifacts missing: $($missingArtifacts.Count)" -ForegroundColor Yellow
}