#Requires -Version 5.0
<#
.SYNOPSIS
Integrates report usage mapping into the unified journey table in field-crosswalk copy 2.md

.DESCRIPTION
- Reads field-to-reports-mapping.csv
- Parses the unified journey table from the Markdown file
- For each field in the journey table, appends the report tags
- Generates an updated Markdown file with report usage populated

.EXAMPLE
.\apply-reports-to-journey-table.ps1
#>

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string]$JourneyTableFile = "field-crosswalk copy 2.md",
    [switch]$Backup
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Load field-to-reports mapping
$mappingFile = Join-Path $TracingFolder "field-to-reports-mapping.csv"
if (-not (Test-Path $mappingFile)) {
    Write-Error "Mapping file not found: $mappingFile"
    exit 1
}

Write-Host "Loading field-to-reports mapping from: $mappingFile" -ForegroundColor Yellow
$fieldReports = @{}
$mappingData = Import-Csv -Path $mappingFile
foreach ($row in $mappingData) {
    $fieldReports[$row.Field] = @{
        Count = [int]$row.ReportCount
        Tags  = $row.ReportTags
    }
}
$uniqueCount = @($fieldReports.Keys).Count
Write-Host "Loaded mapping for $uniqueCount fields" -ForegroundColor Green

# Load journey table from Markdown
$journeyFile = Join-Path $TracingFolder $JourneyTableFile
if (-not (Test-Path $journeyFile)) {
    Write-Error "Journey table file not found: $journeyFile"
    exit 1
}

Write-Host "Reading journey table from: $journeyFile" -ForegroundColor Yellow
$fileContent = Get-Content -Path $journeyFile -Raw

# Create backup if requested
if ($Backup) {
    $backupFile = "$journeyFile.backup.$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -Path $journeyFile -Destination $backupFile
    Write-Host "Backup created: $backupFile" -ForegroundColor Green
}

# Parse journey table section (look for the unified journey table markdown table)
# Pattern: find the table starting with field columns and ending before next section
$tableStartPattern = "^\|\s*Field\s*\|"
$lines = $fileContent -split "`n"

$tableStartIdx = -1
$tableEndIdx = -1

for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match $tableStartPattern) {
        $tableStartIdx = $i
        Write-Host "Found journey table at line $($i + 1)" -ForegroundColor Cyan
        break
    }
}

if ($tableStartIdx -eq -1) {
    Write-Warning "Could not find journey table starting with 'Field' column"
    Write-Host "Showing content around potential table locations..." -ForegroundColor Yellow
    for ($i = 0; $i -lt [Math]::Min($lines.Count, 200); $i++) {
        if ($lines[$i] -match "^\|.*\|") {
            Write-Host "Line $($i + 1): $($lines[$i] -replace '(.{0,80}).*', '$1...')"
        }
    }
    exit 1
}

# Find table end (next heading or section)
for ($i = $tableStartIdx + 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "^##" -or ($lines[$i] -match "^\|" -and $lines[$i] -eq "")) {
        $tableEndIdx = $i - 1
        break
    }
}
if ($tableEndIdx -eq -1) {
    $tableEndIdx = $lines.Count - 1
}

Write-Host "Journey table spans lines $($tableStartIdx + 1) to $($tableEndIdx + 1)" -ForegroundColor Cyan

# Extract header row to find column positions
$headerLine = $lines[$tableStartIdx]
$separatorLine = $lines[$tableStartIdx + 1]

# Split on pipes to identify columns
$headerCols = $headerLine -split '\|' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
Write-Host "Table columns: $($headerCols -join ', ')" -ForegroundColor Yellow

# Check if Reports column exists
$reportsColIdx = [Array]::IndexOf($headerCols, 'Reports')
if ($reportsColIdx -eq -1) {
    Write-Warning "Reports column not found in table. Available columns:"
    for ($i = 0; $i -lt $headerCols.Count; $i++) {
        Write-Host "  [$i] $($headerCols[$i])"
    }
    Write-Host "`nWill attempt to add Reports column..." -ForegroundColor Yellow
}

# Find Field column
$fieldColIdx = [Array]::IndexOf($headerCols, 'Field')
if ($fieldColIdx -eq -1) {
    Write-Error "Could not find Field column in journey table"
    exit 1
}

Write-Host "Field column at index $fieldColIdx, Reports column at index $reportsColIdx" -ForegroundColor Green

# Process table rows and update with report tags
$updatedLines = @($lines[0..($tableStartIdx + 1)])
$matchedFieldsCount = 0
$totalRowsProcessed = 0

for ($i = $tableStartIdx + 2; $i -le $tableEndIdx; $i++) {
    $line = $lines[$i]
    
    # Skip separator rows and empty lines
    if ($line -match "^[\s|]*$" -or $line -match "^[\s-|]+$") {
        $updatedLines += $line
        continue
    }
    
    # Parse row
    if ($line -match "^\|") {
        $totalRowsProcessed++
        $cols = $line -split '\|' | ForEach-Object { $_.Trim() } | Where-Object { $_ }
        
        if ($cols.Count -gt $fieldColIdx) {
            $fieldName = $cols[$fieldColIdx]
            
            # Look up reports for this field
            if ($fieldReports.ContainsKey($fieldName)) {
                $reportInfo = $fieldReports[$fieldName]
                $matchedFieldsCount++
                
                # If Reports column doesn't exist, note for manual review
                if ($reportsColIdx -eq -1) {
                    Write-Verbose "Field '$fieldName' has reports: $($reportInfo.Tags)"
                }
                else {
                    # Update Reports column (placeholder for manual integration)
                    if ($cols.Count -le $reportsColIdx) {
                        # Extend cols array
                        while ($cols.Count -le $reportsColIdx) {
                            $cols += ""
                        }
                    }
                    $cols[$reportsColIdx] = $reportInfo.Tags
                }
            }
        }
        
        # Reconstruct row
        $updatedLine = "| " + ($cols -join " | ") + " |"
        $updatedLines += $updatedLine
    }
    else {
        $updatedLines += $line
    }
}

# Add remaining lines after table
$updatedLines += $lines[($tableEndIdx + 1)..($lines.Count - 1)]

# Report statistics
Write-Host "`n=== Integration Summary ===" -ForegroundColor Cyan
Write-Host "Total rows processed: $totalRowsProcessed"
Write-Host "Fields matched to reports: $matchedFieldsCount"
Write-Host "Total unique fields in mapping: $uniqueCount"

if ($matchedFieldsCount -lt $totalRowsProcessed / 2) {
    Write-Warning "Only $matchedFieldsCount out of $totalRowsProcessed field rows matched. This may indicate:"
    Write-Warning "  - Field names in journey table differ from report output field names"
    Write-Warning "  - Reports column doesn't exist or is in different position"
    Write-Warning "  - Table structure is different than expected"
}

# Save updated content
Write-Host "`nSaving updated journey table..." -ForegroundColor Yellow
$updatedContent = $updatedLines -join "`n"
Set-Content -Path $journeyFile -Value $updatedContent -Encoding UTF8

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $TracingFolder `
    -SourceInputs @($PSCommandPath, $mappingFile) `
    -OutputPaths @($journeyFile)

Write-Host "Journey table updated: $journeyFile" -ForegroundColor Green

Write-Host "`nReport mapping integration complete!" -ForegroundColor Green
Write-Host "Next step: Review the journey table for accuracy in the Reports column"
