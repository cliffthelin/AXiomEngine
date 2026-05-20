#Requires -Version 5.0

param(
    [Parameter(Mandatory = $true)]
    [string]$LeftSnapshotPath,
    [Parameter(Mandatory = $true)]
    [string]$RightSnapshotPath,
    [string]$OutputRoot,
    [switch]$SkipReportWrite
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($OutputRoot)) {
    $OutputRoot = Join-Path (Join-Path $PSScriptRoot 'versions') 'reports'
}

function Resolve-InputPath {
    param([string]$Path)

    if ([string]::IsNullOrWhiteSpace($Path)) {
        throw 'A required path value was empty.'
    }

    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }

    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Path))
}

function Get-SnapshotMetadata {
    param([string]$SnapshotPath)

    $metadataPath = Join-Path $SnapshotPath 'output-traceability.json'
    if (-not (Test-Path -LiteralPath $metadataPath)) {
        throw "Snapshot metadata not found: $metadataPath"
    }

    return Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
}

function Get-PrimaryReviewFiles {
    @(
        'field-crosswalk.md',
        'master-reports-index.json',
        'master-reports-output-lineage.json',
        'clearinghouse-to-report-lineage.csv',
        'lineage-enrichment-summary.md'
    )
}

function Get-HashOrMissing {
    param([string]$Path)

    if (-not (Test-Path -LiteralPath $Path)) {
        return $null
    }

    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash
}

function Normalize-ToArray {
    param([object]$Value)

    if ($null -eq $Value) {
        return @()
    }

    return @($Value)
}

function Get-ListDiff {
    param(
        [object]$Left,
        [object]$Right
    )

    $leftValues = @(Normalize-ToArray -Value $Left | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } | Sort-Object -Unique)
    $rightValues = @(Normalize-ToArray -Value $Right | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) } | Sort-Object -Unique)

    return [pscustomobject]@{
        LeftOnly = @($leftValues | Where-Object { $_ -notin $rightValues })
        RightOnly = @($rightValues | Where-Object { $_ -notin $leftValues })
        Shared = @($leftValues | Where-Object { $_ -in $rightValues })
    }
}

function New-Finding {
    param(
        [string]$Severity,
        [string]$Area,
        [string]$Summary,
        [string]$Detail
    )

    return [pscustomobject]@{
        severity = $Severity
        area = $Area
        summary = $Summary
        detail = $Detail
    }
}

$resolvedLeft = Resolve-InputPath -Path $LeftSnapshotPath
$resolvedRight = Resolve-InputPath -Path $RightSnapshotPath

if (-not (Test-Path -LiteralPath $resolvedLeft)) {
    throw "Left snapshot path not found: $resolvedLeft"
}

if (-not (Test-Path -LiteralPath $resolvedRight)) {
    throw "Right snapshot path not found: $resolvedRight"
}

$leftMeta = Get-SnapshotMetadata -SnapshotPath $resolvedLeft
$rightMeta = Get-SnapshotMetadata -SnapshotPath $resolvedRight

if ($leftMeta.stack_key -ne $rightMeta.stack_key) {
    throw "Snapshots do not share the same stack key. Left=$($leftMeta.stack_key) Right=$($rightMeta.stack_key)"
}

$supports = @()
$findings = @()
$primaryFileResults = @()

$supports += New-Finding -Severity 'info' -Area 'stack-key' -Summary 'Snapshots share the same stack key.' -Detail $leftMeta.stack_key

if ($leftMeta.build_method -ne $rightMeta.build_method) {
    $supports += New-Finding -Severity 'info' -Area 'build-method' -Summary 'Snapshots use different build methods and can be stacked for corroboration.' -Detail ("Left={0}; Right={1}" -f $leftMeta.build_method, $rightMeta.build_method)
}
else {
    $findings += New-Finding -Severity 'medium' -Area 'build-method' -Summary 'Snapshots use the same build method.' -Detail ("Left={0}; Right={1}. This is valid, but it is not a cross-method corroboration pair." -f $leftMeta.build_method, $rightMeta.build_method)
}

if ($leftMeta.manifest_code -eq $rightMeta.manifest_code -and $leftMeta.version -eq $rightMeta.version) {
    $supports += New-Finding -Severity 'info' -Area 'manifest' -Summary 'Manifest identity aligns.' -Detail ("{0} v{1}" -f $leftMeta.manifest_code, $leftMeta.version)
}

$sourceInputDiff = Get-ListDiff -Left $leftMeta.declared_source_inputs -Right $rightMeta.declared_source_inputs
if (@($sourceInputDiff.LeftOnly).Count -eq 0 -and @($sourceInputDiff.RightOnly).Count -eq 0) {
    $supports += New-Finding -Severity 'info' -Area 'source-inputs' -Summary 'Declared additional source inputs match.' -Detail 'No additional source-input conflicts detected.'
}
else {
    $sourceInputDetailParts = @()
    if (@($sourceInputDiff.LeftOnly).Count -gt 0) {
        $sourceInputDetailParts += "Left only: $($sourceInputDiff.LeftOnly -join '; ')"
    }
    if (@($sourceInputDiff.RightOnly).Count -gt 0) {
        $sourceInputDetailParts += "Right only: $($sourceInputDiff.RightOnly -join '; ')"
    }
    $findings += New-Finding -Severity 'medium' -Area 'source-inputs' -Summary 'Declared source inputs differ and should be reviewed.' -Detail ($sourceInputDetailParts -join ' | ')
}

$supportingSnapshotDiff = Get-ListDiff -Left $leftMeta.supporting_snapshots -Right $rightMeta.supporting_snapshots
if (@($supportingSnapshotDiff.Shared).Count -gt 0) {
    $supports += New-Finding -Severity 'info' -Area 'supporting-snapshots' -Summary 'Snapshots reference overlapping supporting snapshots.' -Detail ($supportingSnapshotDiff.Shared -join '; ')
}

foreach ($reviewFile in Get-PrimaryReviewFiles) {
    $leftPath = Join-Path $resolvedLeft $reviewFile
    $rightPath = Join-Path $resolvedRight $reviewFile
    $leftHash = Get-HashOrMissing -Path $leftPath
    $rightHash = Get-HashOrMissing -Path $rightPath

    $status = 'missing'
    $detail = ''

    if ($leftHash -and $rightHash) {
        if ($leftHash -eq $rightHash) {
            $status = 'aligned'
            $detail = 'Hashes match.'
            $supports += New-Finding -Severity 'info' -Area 'primary-file' -Summary ("Primary review file aligns: {0}" -f $reviewFile) -Detail $detail
        }
        else {
            $status = 'conflict'
            $detail = 'Hashes differ.'
            $findings += New-Finding -Severity 'high' -Area 'primary-file' -Summary ("Primary review file differs: {0}" -f $reviewFile) -Detail 'Hashes differ and should be reviewed for support vs contradiction.'
        }
    }
    elseif ($leftHash -or $rightHash) {
        $status = 'coverage-gap'
        $detail = 'File exists in only one snapshot.'
        $findings += New-Finding -Severity 'medium' -Area 'primary-file' -Summary ("Primary review file exists in only one snapshot: {0}" -f $reviewFile) -Detail 'This may indicate coverage expansion, a missing artifact, or a build-method-specific omission.'
    }
    else {
        $status = 'missing-both'
        $detail = 'File missing from both snapshots.'
        $findings += New-Finding -Severity 'low' -Area 'primary-file' -Summary ("Primary review file missing from both snapshots: {0}" -f $reviewFile) -Detail 'No comparison available.'
    }

    $primaryFileResults += [pscustomobject]@{
        file = $reviewFile
        status = $status
        left_path = $leftPath
        right_path = $rightPath
        left_hash = $leftHash
        right_hash = $rightHash
        detail = $detail
    }
}

if (@($findings | Where-Object { $_.severity -eq 'high' }).Count -gt 0) {
    $overallStatus = 'conflict-review-required'
}
elseif (@($findings | Where-Object { $_.severity -eq 'medium' }).Count -gt 0) {
    $overallStatus = 'review-required'
}
else {
    $overallStatus = 'supportive-alignment'
}

$reportBaseName = '{0}__{1}-{2}__vs__{3}-{4}' -f $leftMeta.stack_key, $leftMeta.build_method, $leftMeta.build_scope, $rightMeta.build_method, $rightMeta.build_scope
$safeReportBaseName = ($reportBaseName -replace '[^A-Za-z0-9_.-]', '_')

$supportLines = if (@($supports).Count -gt 0) {
    @($supports | ForEach-Object { '- [{0}] {1} {2}' -f $_.area, $_.summary, $_.detail })
}
else {
    @('- None recorded')
}

$findingLines = if (@($findings).Count -gt 0) {
    @($findings | ForEach-Object { '- [{0}/{1}] {2} {3}' -f $_.severity, $_.area, $_.summary, $_.detail })
}
else {
    @('- None recorded')
}

$primaryReviewLines = @(
    '| File | Status | Detail |',
    '|---|---|---|'
)
$primaryReviewLines += @($primaryFileResults | ForEach-Object { '| {0} | {1} | {2} |' -f $_.file, $_.status, $_.detail })

$sourceInputLeftOnlyText = if (@($sourceInputDiff.LeftOnly).Count -gt 0) { $sourceInputDiff.LeftOnly -join '; ' } else { 'None' }
$sourceInputRightOnlyText = if (@($sourceInputDiff.RightOnly).Count -gt 0) { $sourceInputDiff.RightOnly -join '; ' } else { 'None' }
$sourceInputSharedText = if (@($sourceInputDiff.Shared).Count -gt 0) { $sourceInputDiff.Shared -join '; ' } else { 'None' }
$supportingLeftOnlyText = if (@($supportingSnapshotDiff.LeftOnly).Count -gt 0) { $supportingSnapshotDiff.LeftOnly -join '; ' } else { 'None' }
$supportingRightOnlyText = if (@($supportingSnapshotDiff.RightOnly).Count -gt 0) { $supportingSnapshotDiff.RightOnly -join '; ' } else { 'None' }
$supportingSharedText = if (@($supportingSnapshotDiff.Shared).Count -gt 0) { $supportingSnapshotDiff.Shared -join '; ' } else { 'None' }

$reportLines = @(
    '# Traceability Support Conflict Report',
    '',
    ('- StackKey: {0}' -f $leftMeta.stack_key),
    ('- OverallStatus: {0}' -f $overallStatus),
    ('- LeftSnapshot: {0}' -f $resolvedLeft),
    ('- RightSnapshot: {0}' -f $resolvedRight),
    ('- LeftBuildMethod: {0}' -f $leftMeta.build_method),
    ('- LeftBuildScope: {0}' -f $leftMeta.build_scope),
    ('- RightBuildMethod: {0}' -f $rightMeta.build_method),
    ('- RightBuildScope: {0}' -f $rightMeta.build_scope),
    '',
    '## Support Signals',
    ''
)
$reportLines += $supportLines
$reportLines += @(
    '',
    '## Conflict Or Review Signals',
    ''
)
$reportLines += $findingLines
$reportLines += @(
    '',
    '## Primary Review File Results',
    ''
)
$reportLines += $primaryReviewLines
$reportLines += @(
    '',
    '## Source Input Differences',
    '',
    ('- LeftOnly: {0}' -f $sourceInputLeftOnlyText),
    ('- RightOnly: {0}' -f $sourceInputRightOnlyText),
    ('- Shared: {0}' -f $sourceInputSharedText),
    '',
    '## Supporting Snapshot Differences',
    '',
    ('- LeftOnly: {0}' -f $supportingLeftOnlyText),
    ('- RightOnly: {0}' -f $supportingRightOnlyText),
    ('- Shared: {0}' -f $supportingSharedText)
)

$reportMarkdown = @($reportLines) -join [Environment]::NewLine

$reportObject = [ordered]@{
    stack_key = $leftMeta.stack_key
    overall_status = $overallStatus
    left_snapshot = $resolvedLeft
    right_snapshot = $resolvedRight
    left_build_method = $leftMeta.build_method
    left_build_scope = $leftMeta.build_scope
    right_build_method = $rightMeta.build_method
    right_build_scope = $rightMeta.build_scope
    support_signals = @($supports)
    conflict_signals = @($findings)
    primary_review_files = @($primaryFileResults)
    source_input_diff = $sourceInputDiff
    supporting_snapshot_diff = $supportingSnapshotDiff
}

if (-not $SkipReportWrite) {
    if (-not (Test-Path -LiteralPath $OutputRoot)) {
        $null = New-Item -ItemType Directory -Path $OutputRoot -Force
    }

    $markdownPath = Join-Path $OutputRoot ($safeReportBaseName + '.md')
    $jsonPath = Join-Path $OutputRoot ($safeReportBaseName + '.json')
    Set-Content -LiteralPath $markdownPath -Value $reportMarkdown -Encoding UTF8
    $reportObject | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

    & (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
        -WorkingTraceabilitySource $PSScriptRoot `
        -SourceInputs @($PSCommandPath, $resolvedLeft, $resolvedRight) `
        -OutputPaths @($markdownPath, $jsonPath)

    Write-Host "Report created: $markdownPath" -ForegroundColor Green
    Write-Host "Report created: $jsonPath" -ForegroundColor Green
}

Write-Host "OverallStatus: $overallStatus" -ForegroundColor Green
Write-Host "StackKey: $($leftMeta.stack_key)" -ForegroundColor Green
