#Requires -Version 5.0
<#
.SYNOPSIS
Automates integration of report usage into the unified journey table.
Maps each field to the reports where it appears using master-reports-output-fields-by-field.csv

.DESCRIPTION
- Reads master-reports-output-fields-by-field.csv
- Groups by output_field to find all reports using each field
- Generates a field-to-reports mapping JSON
- Provides lookup function for journey table integration

.EXAMPLE
.\integrate-report-usage.ps1
#>

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [switch]$ExportJSON,
    [switch]$ExportCSV
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# Validate input file
$reportFieldsFile = Join-Path $TracingFolder "master-reports-output-fields-by-field.csv"
if (-not (Test-Path $reportFieldsFile)) {
    Write-Error "Report fields file not found: $reportFieldsFile"
    exit 1
}

Write-Host "Loading report fields from: $reportFieldsFile" -ForegroundColor Yellow
$reportFields = @()
try {
    $reportFields = Import-Csv -Path $reportFieldsFile
    $count = @($reportFields).Count
    Write-Host "Loaded $count report field mappings" -ForegroundColor Green
}
catch {
    Write-Error "Failed to load report fields CSV: $_"
    exit 1
}

# Build field-to-reports mapping
Write-Host "Building field-to-reports mapping..." -ForegroundColor Yellow
$fieldReportMap = @{}

foreach ($row in $reportFields) {
    $field = $row.output_field
    $reportTag = $row.report_tag
    $friendlyName = $row.friendly_name
    
    if (-not $fieldReportMap[$field]) {
        $fieldReportMap[$field] = @()
    }
    
    # Store unique report info (deduplicate by report_tag)
    $existing = $fieldReportMap[$field] | Where-Object { $_.report_tag -eq $reportTag }
    if (-not $existing) {
        $fieldReportMap[$field] += @{
            report_tag    = $reportTag
            friendly_name = $friendlyName
        }
    }
}

$uniqueFieldCount = @($fieldReportMap.Keys).Count
Write-Host "Built mapping for $uniqueFieldCount unique fields" -ForegroundColor Green

# Create summary table
Write-Host "`n=== Field-to-Report Summary ===" -ForegroundColor Cyan
$summary = @()
foreach ($field in $fieldReportMap.Keys | Sort-Object) {
    $reports = $fieldReportMap[$field]
    $reportCount = @($reports).Count
    $reportTags = $reports.report_tag -join "; "
    $summary += [PSCustomObject]@{
        Field       = $field
        ReportCount = $reportCount
        ReportTags  = $reportTags
    }
}

$summary | Format-Table -AutoSize
$summaryCount = @($summary).Count
Write-Host "Total fields with reports: $summaryCount" -ForegroundColor Green

# Export JSON if requested
if ($ExportJSON) {
    $outputJSON = Join-Path $TracingFolder "field-to-reports-mapping.json"
    Write-Host "Exporting field-to-reports mapping as JSON..." -ForegroundColor Yellow
    $jsonMap = @{}
    foreach ($field in $fieldReportMap.Keys) {
        $jsonMap[$field] = @{
            reports = $fieldReportMap[$field]
            count   = @($fieldReportMap[$field]).Count
        }
    }
    $jsonMap | ConvertTo-Json -Depth 10 | Out-File -FilePath $outputJSON -Encoding UTF8
    Write-Host "JSON mapping exported to: $outputJSON" -ForegroundColor Green
}

# Export CSV if requested
if ($ExportCSV) {
    $outputCSV = Join-Path $TracingFolder "field-to-reports-mapping.csv"
    Write-Host "Exporting field-to-reports mapping as CSV..." -ForegroundColor Yellow
    $summary | Export-Csv -Path $outputCSV -NoTypeInformation -Encoding UTF8
    Write-Host "CSV mapping exported to: $outputCSV" -ForegroundColor Green
}

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $TracingFolder `
    -SourceInputs @($PSCommandPath, $reportFieldsFile) `
    -OutputPaths @(
        (Join-Path $TracingFolder 'field-to-reports-mapping.json'),
        (Join-Path $TracingFolder 'field-to-reports-mapping.csv')
    )

# Return mapping as object for pipeline use
$fieldReportMap
