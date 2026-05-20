#Requires -Version 5.0
<#
.SYNOPSIS
Traces field lineage from report outputs back to Clearinghouse input data.

.DESCRIPTION
Creates a bidirectional lineage map showing:
1. Report output field
2. Intermediate transformations and table joins
3. Source STG/PSIS tables and columns
4. Original SIF object and XPath from Clearinghouse
5. Derivation status (direct vs. derived)

.EXAMPLE
.\trace-report-lineage.ps1 -Report "DGW-SSR-0001" -OutputFormat Tree
.\trace-report-lineage.ps1 -Report "LEA-SSR-0018" -Field "LastName" -OutputFormat HTML
.\trace-report-lineage.ps1 -SearchField "LeaNumber" -OutputFormat CSV
#>

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string]$Report,
    [string]$Field,
    [string]$SearchField,
    [ValidateSet('Tree', 'Table', 'HTML', 'JSON', 'CSV')]
    [string]$OutputFormat = 'Tree',
    [switch]$ExportFile
)

# Load artifacts
$lineageFile = Join-Path $TracingFolder "master-reports-output-lineage.json"
$journeyFile = Join-Path $TracingFolder "field-crosswalk copy 2.md"
$fieldMapFile = Join-Path $TracingFolder "field-to-reports-mapping.csv"

Write-Host "Loading lineage artifacts..." -ForegroundColor Yellow

if (-not (Test-Path $lineageFile)) {
    Write-Error "Lineage file not found: $lineageFile"
    exit 1
}

try {
    $lineageData = Get-Content -Path $lineageFile -Raw | ConvertFrom-Json
    Write-Host "Loaded lineage for $(($lineageData | Measure-Object).Count) reports" -ForegroundColor Green
}
catch {
    Write-Error "Failed to parse lineage JSON: $_"
    exit 1
}

# Load journey table mappings
Write-Host "Loading journey table reference..." -ForegroundColor Yellow
$journeyMap = @{}
if (Test-Path $journeyFile) {
    $content = Get-Content -Path $journeyFile -Raw
    $lines = $content -split "`n"
    
    foreach ($line in $lines) {
        if ($line -match "^\| .+ \| .+ \| (.+?) \| .+ \| ([^\|]+?) \| ([^\|]+?) \|") {
            $fieldName = [regex]::Matches($line, '\| ([^\|]+)') | ForEach-Object { $_.Groups[1].Value.Trim() }
            if ($fieldName -and $fieldName.Count -ge 3) {
                $field = $fieldName[2]
                $stgInfo = $fieldName[4]
                $sourceInfo = $fieldName[3]
                
                if ($field -and -not $journeyMap.ContainsKey($field)) {
                    $journeyMap[$field] = @{
                        SIFSource = $sourceInfo
                        STGInfo = $stgInfo
                    }
                }
            }
        }
    }
    Write-Host "Loaded journey table with $(($journeyMap.Keys).Count) field mappings" -ForegroundColor Green
}

# Function to traverse lineage tree
function Trace-LineageTree {
    param(
        [object]$Node,
        [int]$Depth = 0,
        [array]$Path = @()
    )
    
    if (-not $Node) { return @() }
    
    $results = @()
    $indent = "  " * $Depth
    $nodeName = $Node.name
    $nodeType = $Node.node_type
    
    $pathItem = @{
        Depth = $Depth
        Type = $nodeType
        Name = $nodeName
        Table = $Node.table
        Column = $Node.column
        Expression = $Node.expression
    }
    
    $newPath = $Path + @($pathItem)
    
    # If this is a table_column, try to match against journey table
    if ($nodeType -eq 'table_column' -and $Node.column) {
        $match = $journeyMap[$Node.column]
        if ($match) {
            $pathItem['JourneyMatch'] = $match
        }
    }
    
    $results += $pathItem
    
    # Recurse to children
    if ($Node.children) {
        foreach ($child in $Node.children) {
            $results += (Trace-LineageTree -Node $child -Depth ($Depth + 1) -Path $newPath)
        }
    }
    
    return $results
}

# Function to format tree output
function Format-LineageTree {
    param(
        [array]$TracePath,
        [string]$ReportTag,
        [string]$FieldName
    )
    
    Write-Host "`n=== Lineage for $ReportTag :: $FieldName ===" -ForegroundColor Cyan
    Write-Host "Report Output ↓" -ForegroundColor Gray
    
    foreach ($item in $TracePath) {
        $indent = "  " * ($item.Depth + 1)
        $typeColor = switch ($item.Type) {
            'report_output_field' { 'Green' }
            'sql_object' { 'Yellow' }
            'sql_definition' { 'Magenta' }
            'table_column' { 'Cyan' }
            default { 'Gray' }
        }
        
        $display = switch ($item.Type) {
            'report_output_field' { "📊 $($item.Name)" }
            'sql_object' { "🔍 [SQL Query]" }
            'sql_definition' { "→ $($item.Name) = $($item.Expression)" }
            'table_column' { "📋 [$($item.Table)].$($item.Column)" }
            default { $item.Name }
        }
        
        Write-Host "$indent$display" -ForegroundColor $typeColor
        
        # Show journey match if available
        if ($item.JourneyMatch) {
            Write-Host "$indent  ✓ Journey: $($item.JourneyMatch.SIFSource)" -ForegroundColor Green
            Write-Host "$indent    STG: $($item.JourneyMatch.STGInfo)" -ForegroundColor DarkGreen
        }
    }
    
    Write-Host "                   ↓" -ForegroundColor Gray
    Write-Host "        Clearinghouse Input" -ForegroundColor Gray
}

# Function to format table output
function Format-LineageTable {
    param(
        [array]$TracePath,
        [string]$ReportTag,
        [string]$FieldName
    )
    
    $table = @()
    foreach ($item in $TracePath) {
        $table += [PSCustomObject]@{
            Depth = $item.Depth
            Type = $item.Type
            Name = $item.Name
            Table = $item.Table
            Column = $item.Column
            Expression = $item.Expression
            JourneyMatch = if ($item.JourneyMatch) { "✓ $($item.JourneyMatch.SIFSource)" } else { "—" }
        }
    }
    
    Write-Host "`n=== Lineage for $ReportTag :: $FieldName ===" -ForegroundColor Cyan
    $table | Format-Table -AutoSize
}

# Main logic
if ($Report -and $Field) {
    # Trace specific report field
    Write-Host "Tracing lineage for: $Report :: $Field" -ForegroundColor Yellow
    
    $reportData = $lineageData | Where-Object { $_.report_tag -eq $Report }
    if (-not $reportData) {
        Write-Error "Report not found: $Report"
        exit 1
    }
    
    $fieldLineage = $reportData.output_field_lineage | Where-Object { $_.field_name -eq $Field }
    if (-not $fieldLineage) {
        Write-Warning "Field not found in report: $Field"
        Write-Host "Available fields:" -ForegroundColor Gray
        $reportData.output_field_lineage.field_name | Sort-Object -Unique | ForEach-Object { Write-Host "  - $_" }
        exit 1
    }
    
    $tracePath = Trace-LineageTree -Node $fieldLineage.lineage_tree
    
    switch ($OutputFormat) {
        'Tree' { Format-LineageTree -TracePath $tracePath -ReportTag $Report -FieldName $Field }
        'Table' { Format-LineageTable -TracePath $tracePath -ReportTag $Report -FieldName $Field }
    }
}
elseif ($Report) {
    # List all fields in report
    Write-Host "Fields in report: $Report" -ForegroundColor Cyan
    $reportData = $lineageData | Where-Object { $_.report_tag -eq $Report }
    if (-not $reportData) {
        Write-Error "Report not found: $Report"
        exit 1
    }
    
    $fields = $reportData.output_field_lineage | Select-Object field_name, dataset_name | Sort-Object field_name -Unique
    $fields | Format-Table -AutoSize
    
    Write-Host "`nTo trace a specific field:" -ForegroundColor Gray
    Write-Host "  .\trace-report-lineage.ps1 -Report '$Report' -Field '<FieldName>'" -ForegroundColor Gray
}
elseif ($SearchField) {
    # Search for field across all reports
    Write-Host "Searching for field: $SearchField" -ForegroundColor Yellow
    
    $matches = @()
    foreach ($report in $lineageData) {
        $fieldMatches = $report.output_field_lineage | Where-Object { $_.field_name -eq $SearchField }
        foreach ($match in $fieldMatches) {
            $matches += [PSCustomObject]@{
                ReportTag = $report.report_tag
                ReportName = $report.friendly_name
                FieldName = $match.field_name
                Dataset = $match.dataset_name
            }
        }
    }
    
    if ($matches) {
        Write-Host "`nFound in $($matches.Count) reports:" -ForegroundColor Green
        $matches | Format-Table -AutoSize
    }
    else {
        Write-Host "Field not found in any report lineage." -ForegroundColor Yellow
    }
}
else {
    # Show usage
    Write-Host "Report Lineage Tracer" -ForegroundColor Cyan
    Write-Host "`nUsage:" -ForegroundColor Yellow
    Write-Host "  .\trace-report-lineage.ps1 -Report <tag> -Field <name>" -ForegroundColor Gray
    Write-Host "    → Trace lineage for specific report field back to source" -ForegroundColor DarkGray
    Write-Host "`n  .\trace-report-lineage.ps1 -Report <tag>" -ForegroundColor Gray
    Write-Host "    → List all fields in a report" -ForegroundColor DarkGray
    Write-Host "`n  .\trace-report-lineage.ps1 -SearchField <name>" -ForegroundColor Gray
    Write-Host "    → Find which reports use this field" -ForegroundColor DarkGray
    Write-Host "`nExamples:" -ForegroundColor Yellow
    Write-Host "  .\trace-report-lineage.ps1 -Report DGW-SSR-0001 -Field LeaNumber -OutputFormat Tree" -ForegroundColor Gray
    Write-Host "  .\trace-report-lineage.ps1 -SearchField LastName" -ForegroundColor Gray
    exit 0
}
