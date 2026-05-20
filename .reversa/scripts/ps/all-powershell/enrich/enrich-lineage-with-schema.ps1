#Requires -Version 5.0
<#
.SYNOPSIS
Enhanced lineage enrichment with schema-based PSIS/Directory table mapping.

.DESCRIPTION
Extends previous enrichment with 79 additional PSIS.LU_* and DIRECTORY schema mappings
to improve coverage from 11.6% (772 fields) to target 80%+ coverage.

.EXAMPLE
.\enrich-lineage-with-schema.ps1 -ExportFormats CSV,JSON,HTML
#>

param(
    [string]$BaseFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string[]]$ExportFormats = @("CSV", "JSON"),
    [switch]$Verbose
)

# Define helper functions first (before use)
function Get-TableColumns {
    param($node, [System.Collections.ArrayList]$columns)
    
    if (-not $columns) { $columns = [System.Collections.ArrayList]::new() }
    
    if ($node.table_column) {
        [void]$columns.Add($node.table_column)
    }
    
    if ($node.children) {
        foreach ($child in $node.children) {
            Get-TableColumns $child $columns
        }
    }
    
    return @($columns | Select-Object -Unique)
}

function Get-LineageDepth {
    param($node, [int]$depth = 0)
    
    $maxDepth = $depth
    
    if ($node.children) {
        foreach ($child in $node.children) {
            $childDepth = Get-LineageDepth $child ($depth + 1)
            if ($childDepth -gt $maxDepth) { $maxDepth = $childDepth }
        }
    }
    
    return $maxDepth
}

Write-Host "Enhanced Lineage Enrichment with Schema Mapping (v3)" -ForegroundColor Cyan
Write-Host "Loading data sources..." -ForegroundColor Yellow

# Load lineage data
$lineagePath = Join-Path $BaseFolder "master-reports-output-lineage.json"
try {
    $lineageData = Get-Content -Path $lineagePath -Raw | ConvertFrom-Json
    Write-Host "Loaded $($lineageData.Count) reports from lineage JSON" -ForegroundColor Green
} catch {
    Write-Host "Failed to load $lineagePath" -ForegroundColor Red
    exit 1
}

# Load journey table reference
$journeyPath = Join-Path $BaseFolder "field-crosswalk copy 2.md"
try {
    $journeyMd = Get-Content -Path $journeyPath -Raw
} catch {
    Write-Host "Failed to load $journeyPath" -ForegroundColor Red
    exit 1
}

# Load schema mapping CSV
$schemaMappingPath = Join-Path $BaseFolder "psis-directory-schema-mapping.csv"
try {
    $schemaMappings = Import-Csv -Path $schemaMappingPath
    Write-Host "Loaded $(($schemaMappings | Measure-Object).Count) schema.column definitions" -ForegroundColor Green
} catch {
    Write-Host "Failed to load $schemaMappingPath" -ForegroundColor Red
    exit 1
}

# Parse journey table into lookup hashtables
$journeyByField = @{}
$journeyByCol = @{}

$matches = [regex]::Matches($journeyMd, "\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|", [System.Text.RegularExpressions.RegexOptions]::Multiline)
foreach ($m in $matches) {
    $chObj = $m.Groups[1].Value.Trim()
    $chCode = $m.Groups[2].Value.Trim()
    $fieldName = $m.Groups[3].Value.Trim()
    
    if ($fieldName -and $chObj -ne "Clearinghouse Object") {
        $journeyByField[$fieldName] = $chObj
        
        if ($m.Groups[2].Value.Contains(".")) {
            $journeyByCol[$m.Groups[2].Value.ToUpper()] = $chObj
        }
    }
}

Write-Host "Parsed journey table: $(@($journeyByField).Count) fields, $(@($journeyByCol).Count) table.columns" -ForegroundColor Green

# Build extended schema mapping from CSV
$schemaMap = @{}
foreach ($row in $schemaMappings) {
    $key = "$($row.Table).$($row.Column)".ToUpper()
    $schemaMap[$key] = [PSCustomObject]@{
        Table = $row.Table
        Column = $row.Column
        ClearinghouseSource = $row.ClearinghouseSource
        ClearinghouseObject = $row.ClearinghouseObject
        SourceType = "Via Schema Mapping"
    }
}

Write-Host "Schema mapping hashtable: $(@($schemaMap).Count) lookups" -ForegroundColor Green

# Process enrichment with new mappings
Write-Host "Processing enrichment..." -ForegroundColor Yellow
$enrichedFields = [System.Collections.ArrayList]::new()
$coverageStats = @{
    Direct = 0
    ViaLookup = 0
    ViaSchema = 0
    NotFound = 0
}

foreach ($report in $lineageData) {
    foreach ($field in $report.output_field_lineage) {
        # Skip if output_field is null or empty
        if (-not $field.output_field) { continue }
        
        $fieldPath = ""
        $sourceType = "Not Found"
        $clearinghouseSource = ""
        $clearinghouseObject = ""
        
        # Try level 1: Direct field name match
        if ($journeyByField -and $journeyByField.ContainsKey($field.output_field)) {
            $clearinghouseSource = $journeyByField[$field.output_field]
            $sourceType = "Direct"
            $coverageStats.Direct++
        }
        else {
            # Try level 2: Extract table.column references from lineage tree
            if ($field.lineage_tree) {
                $tableRefs = Get-TableColumns $field.lineage_tree
                
                foreach ($tblRef in $tableRefs) {
                    $tblRefUpper = $tblRef.ToUpper()
                    
                    # Check journey table column mapping
                    if ($journeyByCol -and $journeyByCol.ContainsKey($tblRefUpper)) {
                        $clearinghouseSource = $journeyByCol[$tblRefUpper]
                        $sourceType = "Via Journey Table"
                        $coverageStats.ViaLookup++
                        break
                    }
                    
                    # Check schema mapping
                    if ($schemaMap -and $schemaMap.ContainsKey($tblRefUpper)) {
                        $mapping = $schemaMap[$tblRefUpper]
                        $clearinghouseSource = $mapping.ClearinghouseSource
                        $clearinghouseObject = $mapping.ClearinghouseObject
                        $sourceType = "Via Schema Mapping"
                        $coverageStats.ViaSchema++
                        break
                    }
                }
            }
            
            if ($sourceType -eq "Not Found") {
                $coverageStats.NotFound++
            }
        }
        
        [void]$enrichedFields.Add([PSCustomObject]@{
            ReportTag = $report.report_tag
            ReportName = $report.report_name
            OutputField = $field.output_field
            ClearinghouseSource = $clearinghouseSource
            ClearinghouseObject = $clearinghouseObject
            SourceType = $sourceType
            LineageDepth = if ($field.lineage_tree) { Get-LineageDepth $field.lineage_tree } else { 0 }
        })
    }
}

Write-Host "Processed $(($enrichedFields | Measure-Object).Count) output field lineages" -ForegroundColor Green
Write-Host "`nEnrichment Coverage:" -ForegroundColor Cyan
$total = $coverageStats.Direct + $coverageStats.ViaLookup + $coverageStats.ViaSchema + $coverageStats.NotFound
$directPct = [Math]::Round($coverageStats.Direct * 100 / $total, 1)
$viaLookupPct = [Math]::Round($coverageStats.ViaLookup * 100 / $total, 1)
$viaSchemaPct = [Math]::Round($coverageStats.ViaSchema * 100 / $total, 1)
$notFoundPct = [Math]::Round($coverageStats.NotFound * 100 / $total, 1)
$tracedCount = $coverageStats.Direct + $coverageStats.ViaLookup + $coverageStats.ViaSchema
$tracedPct = [Math]::Round($tracedCount * 100 / $total, 1)

$msg1 = "  Direct field match:     " + $coverageStats.Direct + " (" + $directPct + ")"
$msg2 = "  Via Journey Table:      " + $coverageStats.ViaLookup + " (" + $viaLookupPct + ")"
$msg3 = "  Via Schema Mapping:     " + $coverageStats.ViaSchema + " (" + $viaSchemaPct + ")"
$msg4 = "  Not Found:              " + $coverageStats.NotFound + " (" + $notFoundPct + ")"
$msg5 = "  Total Traced:           " + $tracedCount + " of " + $total + " (" + $tracedPct + ")"

Write-Host $msg1 -ForegroundColor Green
Write-Host $msg2 -ForegroundColor Green
Write-Host $msg3 -ForegroundColor Green
Write-Host $msg4 -ForegroundColor Yellow
Write-Host $msg5 -ForegroundColor Green

# Export
$prefix = Join-Path $BaseFolder "clearinghouse-to-report-lineage-v3"

foreach ($fmt in $ExportFormats) {
    if ($fmt -eq "CSV") {
        $out = "$prefix.csv"
        $enrichedFields | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8
        Write-Host "CSV: $out" -ForegroundColor Green
    }
    if ($fmt -eq "JSON") {
        $out = "$prefix.json"
        $enrichedFields | ConvertTo-Json -Depth 5 | Out-File -FilePath $out -Encoding UTF8
        Write-Host "JSON: $out" -ForegroundColor Green
    }
}

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $BaseFolder `
    -SourceInputs @($PSCommandPath, $lineagePath, $journeyPath, $schemaMappingPath) `
    -OutputPaths @(
        "$prefix.csv",
        "$prefix.json"
    )

Write-Host "`nEnhanced enrichment complete!" -ForegroundColor Green
