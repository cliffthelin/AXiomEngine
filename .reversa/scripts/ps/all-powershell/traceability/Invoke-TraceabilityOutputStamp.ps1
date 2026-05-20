#Requires -Version 5.0

param(
    [string[]]$OutputPaths = @(),
    [string]$WorkingTraceabilitySource,
    [string[]]$SourceInputs = @(),
    [ValidateSet('module', 'feature', 'combined', 'unspecified')]
    [string]$BuildMethod = 'unspecified',
    [string]$BuildScope = 'unspecified'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$helperPath = Join-Path $PSScriptRoot 'Set-TraceabilityOutputProvenance.ps1'
if (-not (Test-Path -LiteralPath $helperPath)) {
    throw "Provenance helper not found: $helperPath"
}

if ([string]::IsNullOrWhiteSpace($WorkingTraceabilitySource)) {
    $WorkingTraceabilitySource = $PSScriptRoot
}

$groupedOutputs = @{}
foreach ($outputPath in @($OutputPaths | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })) {
    if (-not (Test-Path -LiteralPath $outputPath)) {
        continue
    }

    $resolvedPath = [System.IO.Path]::GetFullPath($outputPath)
    $targetFolder = Split-Path -Parent $resolvedPath
    $artifactFile = Split-Path -Leaf $resolvedPath

    if (-not $groupedOutputs.ContainsKey($targetFolder)) {
        $groupedOutputs[$targetFolder] = New-Object System.Collections.Generic.List[string]
    }

    if ($artifactFile -notin $groupedOutputs[$targetFolder]) {
        [void]$groupedOutputs[$targetFolder].Add($artifactFile)
    }
}

foreach ($targetFolder in $groupedOutputs.Keys) {
    & $helperPath `
        -TargetFolder $targetFolder `
        -WorkingTraceabilitySource $WorkingTraceabilitySource `
        -SourceInputs @($SourceInputs | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }) `
        -BuildMethod $BuildMethod `
        -BuildScope $BuildScope `
        -ArtifactFiles ($groupedOutputs[$targetFolder].ToArray()) | Out-Null
}
