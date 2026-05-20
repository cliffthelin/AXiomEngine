#Requires -Version 5.0

param(
    [string]$VersionsRoot,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($VersionsRoot)) {
    $VersionsRoot = Join-Path $PSScriptRoot 'versions'
}

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $VersionsRoot 'INDEX.md'
}

function Get-SnapshotDirectories {
    param(
        [string]$Root
    )

    $snapshotDirs = New-Object System.Collections.Generic.List[object]

    foreach ($entry in Get-ChildItem -LiteralPath $Root -Directory) {
        if ($entry.Name -eq 'reports') {
            continue
        }

        $metadataPath = Join-Path $entry.FullName 'output-traceability.json'
        if (Test-Path -LiteralPath $metadataPath) {
            [void]$snapshotDirs.Add($entry)
            continue
        }

        foreach ($nestedEntry in Get-ChildItem -LiteralPath $entry.FullName -Directory -ErrorAction SilentlyContinue) {
            $nestedMetadataPath = Join-Path $nestedEntry.FullName 'output-traceability.json'
            if (Test-Path -LiteralPath $nestedMetadataPath) {
                [void]$snapshotDirs.Add($nestedEntry)
            }
        }
    }

    return $snapshotDirs.ToArray()
}

$snapshotDirs = Get-SnapshotDirectories -Root $VersionsRoot
$snapshots = foreach ($snapshotDir in $snapshotDirs) {
    $metadataPath = Join-Path $snapshotDir.FullName 'output-traceability.json'
    $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
    [pscustomobject]@{
        SnapshotPath = $snapshotDir.FullName
        SnapshotName = $snapshotDir.Name
        BuildMethod = $metadata.build_method
        BuildScope = $metadata.build_scope
        ManifestCode = $metadata.manifest_code
        Version = $metadata.version
        StackKey = $metadata.stack_key
        SourceInputCount = @($metadata.declared_source_inputs).Count
        SupportingSnapshotCount = @($metadata.supporting_snapshots).Count
    }
}

$stackGroups = @($snapshots | Group-Object StackKey | Sort-Object Name)

$lines = New-Object System.Collections.Generic.List[string]
[void]$lines.Add('# Traceability Versions Index')
[void]$lines.Add('')
[void]$lines.Add(('Generated: {0}' -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')))
[void]$lines.Add('')
[void]$lines.Add('## Snapshot Summary')
[void]$lines.Add('')
[void]$lines.Add(('Total snapshots: {0}' -f @($snapshots).Count))
[void]$lines.Add(('Distinct stack keys: {0}' -f @($stackGroups).Count))
[void]$lines.Add('')
[void]$lines.Add('## All Snapshots')
[void]$lines.Add('')
[void]$lines.Add('| StackKey | BuildMethod | BuildScope | ManifestCode | Version | SourceInputs | SupportingSnapshots | SnapshotPath |')
[void]$lines.Add('|---|---|---|---|---|---|---|---|')
foreach ($snapshot in ($snapshots | Sort-Object StackKey, BuildMethod, BuildScope, SnapshotName)) {
    [void]$lines.Add(("| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} |" -f $snapshot.StackKey, $snapshot.BuildMethod, $snapshot.BuildScope, $snapshot.ManifestCode, $snapshot.Version, $snapshot.SourceInputCount, $snapshot.SupportingSnapshotCount, $snapshot.SnapshotPath.Replace('\', '/')))
}

[void]$lines.Add('')
[void]$lines.Add('## Correlation By Stack Key')
[void]$lines.Add('')
foreach ($stackGroup in $stackGroups) {
    [void]$lines.Add(('### {0}' -f $stackGroup.Name))
    [void]$lines.Add('')
    [void]$lines.Add('| BuildMethod | BuildScope | SnapshotPath |')
    [void]$lines.Add('|---|---|---|')
    foreach ($item in ($stackGroup.Group | Sort-Object BuildMethod, BuildScope, SnapshotName)) {
        [void]$lines.Add(("| {0} | {1} | {2} |" -f $item.BuildMethod, $item.BuildScope, $item.SnapshotPath.Replace('\', '/')))
    }
    [void]$lines.Add('')
}

[void]$lines.Add('## How To Compare')
[void]$lines.Add('')
[void]$lines.Add('Use Compare-TraceabilitySnapshots.ps1 with two snapshots that share the same stack key.')
[void]$lines.Add('')
[void]$lines.Add('Example:')
[void]$lines.Add('')
[void]$lines.Add('```powershell')
[void]$lines.Add('.\Compare-TraceabilitySnapshots.ps1 -LeftSnapshotPath "versions/module/2026UTREX__v14.21" -RightSnapshotPath "versions/feature/2026UTREX__v14.21"')
[void]$lines.Add('```')

Set-Content -LiteralPath $OutputPath -Value ($lines -join [Environment]::NewLine) -Encoding UTF8

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $PSScriptRoot `
    -SourceInputs @($PSCommandPath, $VersionsRoot) `
    -OutputPaths @($OutputPath)

Write-Host "Index created: $OutputPath" -ForegroundColor Green
