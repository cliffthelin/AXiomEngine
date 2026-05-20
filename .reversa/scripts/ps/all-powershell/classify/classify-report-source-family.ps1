#Requires -Version 5.0

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string[]]$ExportFormats = @("CSV", "JSON")
)

function Test-MeaningfulValue {
    param([string]$Value)

    if ([string]::IsNullOrWhiteSpace($Value)) { return $false }

    $trimmed = $Value.Trim()
    if ($trimmed -in @("-", "--", "---", "UPASSField", "FinalizerField")) { return $false }

    return $true
}

function Join-UniqueValues {
    param([System.Collections.IEnumerable]$Values)

    $items = @()
    foreach ($value in $Values) {
        if ([string]::IsNullOrWhiteSpace([string]$value)) { continue }
        $text = [string]$value
        if ($items -notcontains $text) {
            $items += $text
        }
    }

    return ($items -join "; ")
}

Write-Host "Report Field Source Family Classifier" -ForegroundColor Cyan

$lineagePath = Join-Path $TracingFolder "clearinghouse-to-report-lineage.csv"
$buildPath = Join-Path $TracingFolder "master-reports-build-fields-by-field.csv"
$journeyPath = Join-Path $TracingFolder "field-crosswalk copy 2.md"

if (-not (Test-Path $lineagePath)) { throw "Missing lineage file: $lineagePath" }
if (-not (Test-Path $buildPath)) { throw "Missing build fields file: $buildPath" }
if (-not (Test-Path $journeyPath)) { throw "Missing journey file: $journeyPath" }

$lineageRows = Import-Csv -Path $lineagePath
$buildRows = Import-Csv -Path $buildPath

Write-Host "Loaded $($lineageRows.Count) lineage rows" -ForegroundColor Green
Write-Host "Loaded $($buildRows.Count) build-field rows" -ForegroundColor Green

$buildFieldsByReport = @{}
foreach ($row in $buildRows) {
    if (-not $buildFieldsByReport.ContainsKey($row.report_tag)) {
        $buildFieldsByReport[$row.report_tag] = New-Object System.Collections.ArrayList
    }
    [void]$buildFieldsByReport[$row.report_tag].Add($row.build_field)
}

$journeyByField = @{}
$journeyLines = Get-Content -Path $journeyPath -Encoding UTF8
$headerSeen = $false

foreach ($line in $journeyLines) {
    if ($line -notmatch '^\|') { continue }

    $cells = ($line -split '\|') | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
    if ($cells.Count -lt 13) { continue }

    if ($cells[0] -eq "Clearinghouse Object") {
        $headerSeen = $true
        continue
    }

    if (-not $headerSeen) { continue }
    if ($cells[0] -match '^-+$') { continue }

    $fieldName = $cells[2]
    $upassValue = $cells[11]

    if ([string]::IsNullOrWhiteSpace($fieldName)) { continue }
    if (-not $journeyByField.ContainsKey($fieldName)) {
        $journeyByField[$fieldName] = $upassValue
    }
}

Write-Host "Parsed $($journeyByField.Count) journey field mappings" -ForegroundColor Green

$classified = New-Object System.Collections.ArrayList

foreach ($row in $lineageRows) {
    $buildFields = @()
    if ($buildFieldsByReport.ContainsKey($row.ReportTag)) {
        $buildFields = @($buildFieldsByReport[$row.ReportTag])
    }

    $buildEvidence = Join-UniqueValues -Values $buildFields
    $upassPath = ""
    if ($journeyByField.ContainsKey($row.OutputField)) {
        $upassPath = $journeyByField[$row.OutputField]
    }

    $intermediate = [string]$row.IntermediateFields
    $stgTable = [string]$row.STGTable
    $psisInfo = [string]$row.PSISInfo

    $hasWarehouse = ($intermediate -match '(?i)(^|[; ,])(?:[A-Za-z0-9_]+\.)?dbo\.' -or $buildEvidence -match '(?i)(^|[; ,])(?:[A-Za-z0-9_]+\.)?dbo\.')
    $hasCactus = ($row.OutputField -match '(?i)CACTUS' -or
        $intermediate -match '(?i)(RODS(?:-DB-P-W1)?\.USBEData(?:\.\[?USBEData\]?)?\.CACTUS\.|RODS\.USBEData\.CACTUS\.|\bCACTUS\.dbo_|\bCACTUS\.)' -or
        $buildEvidence -match '(?i)(RODS(?:-DB-P-W1)?\.USBEData(?:\.\[?USBEData\]?)?\.CACTUS\.|RODS\.USBEData\.CACTUS\.|\bCACTUS\.dbo_|\bCACTUS\.)')
    $hasDibels = ($intermediate -match '(?i)DIBELS\.dbo\.' -or $buildEvidence -match '(?i)DIBELS\.dbo\.')
    $hasUtrex = ($stgTable -match '(?i)^PSIS\.Stg_' -or $psisInfo -match '(?i)PSIS\.|DIRECTORY\.' -or $buildEvidence -match '(?i)PSIS\.|DIRECTORY\.|Directory\.')
    $hasUpassPath = (Test-MeaningfulValue -Value $upassPath)
    $hasFabric = ($upassPath -match '(?i)be_upass|bronze_|silver_|gold_' -or $intermediate -match '(?i)be_upass|bronze_|silver_|gold_' -or $buildEvidence -match '(?i)be_upass|bronze_|silver_|gold_')
    $hasUpass = ($hasUpassPath -or $hasFabric)

    $sourceFamily = "Unknown"
    if ($hasWarehouse -and $hasUtrex -and $hasCactus) {
        $sourceFamily = "Warehouse fed by UTREx and CACTUS"
    }
    elseif ($hasWarehouse -and $hasCactus) {
        $sourceFamily = "Warehouse fed by CACTUS"
    }
    elseif ($hasUtrex -and $hasCactus) {
        $sourceFamily = "UTREx with CACTUS"
    }
    elseif ($hasWarehouse -and $hasUtrex) {
        $sourceFamily = "Warehouse fed by UTREx"
    }
    elseif ($hasWarehouse -and $hasUpass) {
        $sourceFamily = "Warehouse with UPASS path"
    }
    elseif ($hasUtrex -and $hasUpass) {
        $sourceFamily = "UTREx with UPASS path"
    }
    elseif ($hasWarehouse) {
        $sourceFamily = if ($hasDibels) { "DIBELS Warehouse" } else { "Data Warehouse" }
    }
    elseif ($hasCactus) {
        $sourceFamily = "CACTUS/RODS"
    }
    elseif ($hasUtrex) {
        $sourceFamily = "UTREx/PSIS"
    }
    elseif ($hasUpass) {
        $sourceFamily = "UPASS/Fabric"
    }

    $evidence = @()
    if ($hasWarehouse) { $evidence += "warehouse" }
    if ($hasCactus) { $evidence += "cactus" }
    if ($hasDibels) { $evidence += "dibels" }
    if ($hasUtrex) { $evidence += "utrex" }
    if ($hasUpassPath) { $evidence += "journey-upass" }
    if ($hasFabric) { $evidence += "fabric-upass" }

    $confidence = switch ($evidence.Count) {
        { $_ -ge 3 } { "High"; break }
        2 { "Medium"; break }
        1 { "Low"; break }
        default { "Low" }
    }

    $nextTraceTarget = switch ($sourceFamily) {
        "Warehouse fed by UTREx and CACTUS" { "Open the warehouse object first, then split the joins into PSIS/STG lineage and CACTUS/RODS lineage branches." }
        "Warehouse fed by CACTUS" { "Open the warehouse object first, then trace the CACTUS join back to RODS.USBEData.CACTUS source tables." }
        "UTREx with CACTUS" { "Start at the report SQL join boundary and separate which columns come from PSIS/DIRECTORY versus CACTUS/RODS." }
        "Warehouse fed by UTREx" { "Open the warehouse view/table definition first, then follow joins back to PSIS/STG columns." }
        "Warehouse with UPASS path" { "Check whether the report reads warehouse tables that are loaded from be_upass or Fabric gold." }
        "UTREx with UPASS path" { "Start at the PSIS/DIRECTORY column, then verify whether the same field is later published into be_upass." }
        "Data Warehouse" { "Trace the dbo object to its ETL/view definition to see whether it originates from UTREx, UPASS, or a warehouse-only calculation." }
        "CACTUS/RODS" { "Trace the field to the RODS.USBEData.CACTUS source object, then determine whether the report uses it directly or through a warehouse sync." }
        "DIBELS Warehouse" { "Trace the DIBELS warehouse table first, then inspect how it joins back to core warehouse or UTREx dimensions." }
        "UTREx/PSIS" { "Map the PSIS/DIRECTORY column back to STG and then to the SIF source object." }
        "UPASS/Fabric" { "Trace the be_upass or Fabric gold field back through silver/bronze and then to the inbound SIF/R_* source." }
        default { "Use the report SQL and RDL dataset to find the first concrete table or view reference." }
    }

    [void]$classified.Add([PSCustomObject]@{
        ReportTag = $row.ReportTag
        ReportName = $row.ReportName
        OutputField = $row.OutputField
        SourceType = $row.SourceType
        SourceFamily = $sourceFamily
        Confidence = $confidence
        HasWarehouseEvidence = $hasWarehouse
        HasCACTUSEvidence = $hasCactus
        HasUTRExEvidence = $hasUtrex
        HasUPASSPath = $hasUpass
        STGTable = $row.STGTable
        PSISInfo = $row.PSISInfo
        IntermediateFields = $row.IntermediateFields
        ReportBuildFields = $buildEvidence
        JourneyUPASSPath = $upassPath
        EvidenceTags = (Join-UniqueValues -Values $evidence)
        NextTraceTarget = $nextTraceTarget
    })
}

$summary = $classified | Group-Object SourceFamily | Sort-Object Count -Descending
Write-Host "" 
Write-Host "Source family summary:" -ForegroundColor Cyan
foreach ($group in $summary) {
    Write-Host (("  {0}: {1}" -f $group.Name, $group.Count)) -ForegroundColor Green
}

$prefix = Join-Path $TracingFolder "report-field-source-family"
if ($ExportFormats -contains "CSV") {
    $csvPath = "$prefix.csv"
    $classified | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
    Write-Host "CSV: $csvPath" -ForegroundColor Green
}
if ($ExportFormats -contains "JSON") {
    $jsonPath = "$prefix.json"
    $classified | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonPath -Encoding UTF8
    Write-Host "JSON: $jsonPath" -ForegroundColor Green
}

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $TracingFolder `
    -SourceInputs @($PSCommandPath, $lineagePath, $buildPath, $journeyTablePath) `
    -OutputPaths @(
        "$prefix.csv",
        "$prefix.json"
    )
