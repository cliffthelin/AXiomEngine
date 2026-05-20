#Requires -Version 5.0
<#
.SYNOPSIS
Populates the Reports/Usage column in the Unified End-to-End Field Journey Table with actual report tags.

.DESCRIPTION
- Reads the field-to-reports-mapping.csv
- Finds the unified journey table in field-crosswalk copy 2.md
- Matches "Field Name" column entries to the mapping
- Replaces placeholder text in the Reports/Usage column with actual report tags
- Preserves table structure and markdown formatting

.EXAMPLE
.\populate-reports-in-journey-table.ps1 -Preview
.\populate-reports-in-journey-table.ps1 -Apply
#>

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string]$JourneyTableFile = "field-crosswalk copy 2.md",
    [switch]$Preview,
    [switch]$Apply,
    [switch]$Backup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Validate mode
if (-not $Preview -and -not $Apply) {
    Write-Host "Usage: .\populate-reports-in-journey-table.ps1 [-Preview] [-Apply] [-Backup]" -ForegroundColor Yellow
    Write-Host "  -Preview : Show what would be changed (default)" -ForegroundColor Gray
    Write-Host "  -Apply   : Actually modify the file" -ForegroundColor Gray
    Write-Host "  -Backup  : Create a backup before applying changes" -ForegroundColor Gray
    exit 1
}

# Load field-to-reports mapping
$mappingFile = Join-Path $TracingFolder "field-to-reports-mapping.csv"
if (-not (Test-Path $mappingFile)) {
    Write-Error "Mapping file not found: $mappingFile"
    exit 1
}

Write-Host "Loading field-to-reports mapping..." -ForegroundColor Yellow
$fieldReportsMap = @{}
$mappingData = Import-Csv -Path $mappingFile
foreach ($row in $mappingData) {
    $fieldReportsMap[$row.Field] = $row.ReportTags
}
Write-Host "Loaded $(($fieldReportsMap.Keys).Count) field mappings" -ForegroundColor Green

# Load journey table
$journeyFile = Join-Path $TracingFolder $JourneyTableFile
if (-not (Test-Path $journeyFile)) {
    Write-Error "Journey table file not found: $journeyFile"
    exit 1
}

Write-Host "Reading journey table from: $journeyFile" -ForegroundColor Yellow
$fileContent = Get-Content -Path $journeyFile -Raw
$lines = $fileContent -split "`n"

# Find unified journey table section
Write-Host "Locating unified journey table..." -ForegroundColor Yellow
$tableStartIdx = -1
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^# Unified End-to-End Field Journey Table") {
        $tableStartIdx = $i
        Write-Host "Found table header at line $($i + 1)" -ForegroundColor Cyan
        break
    }
}

if ($tableStartIdx -eq -1) {
    Write-Error "Could not find 'Unified End-to-End Field Journey Table' section"
    exit 1
}

# Find the header line (starts with pipe)
$headerLineIdx = -1
for ($i = $tableStartIdx; $i -lt [Math]::Min($tableStartIdx + 10, $lines.Count); $i++) {
    if ($lines[$i] -match "^\| Clearinghouse Object") {
        $headerLineIdx = $i
        Write-Host "Found table header row at line $($i + 1)" -ForegroundColor Cyan
        break
    }
}

if ($headerLineIdx -eq -1) {
    Write-Error "Could not find table header row with pipe delimiters"
    exit 1
}

# Parse header to find column indices
$headerLine = $lines[$headerLineIdx]
$columns = $headerLine -split '\|' | ForEach-Object { $_.Trim() }
$fieldNameIdx = [Array]::IndexOf($columns, 'Field Name')
$reportUsageIdx = [Array]::IndexOf($columns, 'Reports/Usage')

Write-Host "Header columns: $($columns.Count)" -ForegroundColor Cyan
Write-Host "  Field Name at index: $fieldNameIdx" -ForegroundColor Gray
Write-Host "  Reports/Usage at index: $reportUsageIdx" -ForegroundColor Gray

if ($fieldNameIdx -eq -1 -or $reportUsageIdx -eq -1) {
    Write-Error "Could not locate Field Name or Reports/Usage column"
    exit 1
}

# Process table rows (start after header and separator)
$separatorIdx = $headerLineIdx + 1
$updateCount = 0
$matchCount = 0
$updatedLines = @()

# Copy everything up to and including the header + separator
$updatedLines = $lines[0..$separatorIdx]

# Process data rows
for ($i = $separatorIdx + 1; $i -lt $lines.Count; $i++) {
    $line = $lines[$i]
    
    # Stop at next section (heading) or end of table
    if ($line -match "^#" -or $line -match "^    ▼") {
        $updatedLines += $lines[$i..$($lines.Count - 1)]
        break
    }
    
    # Skip non-table rows
    if (-not ($line -match "^\|")) {
        $updatedLines += $line
        continue
    }
    
    # Parse table row
    $cells = $line -split '\|' | ForEach-Object { $_.Trim() }
    
    # Skip if not enough columns
    if ($cells.Count -le [Math]::Max($fieldNameIdx, $reportUsageIdx)) {
        $updatedLines += $line
        continue
    }
    
    $fieldName = $cells[$fieldNameIdx]
    $currentReports = $cells[$reportUsageIdx]
    
    # Look up field in mapping
    if ($fieldReportsMap.ContainsKey($fieldName)) {
        $newReports = $fieldReportsMap[$fieldName]
        $matchCount++
        
        if ($currentReports -ne $newReports) {
            $updateCount++
            $cells[$reportUsageIdx] = $newReports
            
            if ($Preview) {
                Write-Host "  [$fieldName] → $($newReports.Substring(0, [Math]::Min(80, $newReports.Length)))..." -ForegroundColor Green
            }
        }
    }
    
    # Reconstruct row
    $newLine = "| " + ($cells -join " | ") + " |"
    $updatedLines += $newLine
}

# Output statistics
Write-Host "`n=== Population Summary ===" -ForegroundColor Cyan
Write-Host "Fields matched to reports: $matchCount"
Write-Host "Rows updated: $updateCount"

if ($updateCount -gt 0 -and $Apply) {
    # Create backup if requested
    if ($Backup) {
        $backupFile = "$journeyFile.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Copy-Item -Path $journeyFile -Destination $backupFile
        Write-Host "Backup created: $backupFile" -ForegroundColor Green
    }
    
    # Save updated content
    Write-Host "`nSaving updated journey table..." -ForegroundColor Yellow
    $updatedContent = $updatedLines -join "`n"
    Set-Content -Path $journeyFile -Value $updatedContent -Encoding UTF8 -Force

    & (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
        -WorkingTraceabilitySource $TracingFolder `
        -SourceInputs @($PSCommandPath, $mappingFile) `
        -OutputPaths @($journeyFile)

    Write-Host "Journey table updated: $journeyFile" -ForegroundColor Green
    Write-Host "Updated $updateCount rows with report usage information" -ForegroundColor Green
}
elseif ($Preview) {
    Write-Host "`nPreview mode: No changes made. Use -Apply to save changes." -ForegroundColor Yellow
}
else {
    Write-Host "`nNo updates needed or changes not applied." -ForegroundColor Yellow
}

Write-Host "`nReport mapping integration complete!" -ForegroundColor Green
