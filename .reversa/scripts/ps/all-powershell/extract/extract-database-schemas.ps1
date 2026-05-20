#Requires -Version 5.0
<#
.SYNOPSIS
Extracts and catalogs database schemas from UTREx and related repos to support lineage tracing.

.DESCRIPTION
- Scans for SQL table definitions (CREATE TABLE statements)
- Extracts table name, columns, data types, and extended properties
- Creates searchable lookup artifacts for lineage enrichment
- Outputs CSV and JSON for report-to-clearinghouse field mapping

.EXAMPLE
.\extract-database-schemas.ps1 -Repos @("UTREx-develop", "FinalizerService-develop") -Output CSV,JSON
#>

param(
    [string]$WorkspacePath = "c:\Projects\GITHUB",
    [string[]]$Repos = @("UTREx-develop", "FinalizerService-develop", "Data-Gateway-develop"),
    [string[]]$Output = @("CSV", "JSON"),
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Database Schema Extraction Tool" -ForegroundColor Cyan

# Key tables we need to trace back to Clearinghouse
$targetTables = @(
    "PSIS.GRADE_MEMBERSHIP", "PSIS.PSIS_DISTRICT_MEMBERSHIP", "PSIS.PSIS_PRI_FAC_MEMBERSHIP",
    "PSIS.LU_EXIT_TYPE", "PSIS.LU_LIMITED_ENGLISH", "PSIS.LU_RESIDENT_STATUS", 
    "PSIS.LU_FREE_RED_LUNCH", "PSIS.LU_HOMELESS", "PSIS.LU_HIGH_SCHOOL_COMPL_STATUS",
    "PSIS.LU_SCRAM_DISABILITY_CODES", "PSIS.LU_SCRAM_ENVIRONMENT_CODES", 
    "PSIS.PSIS_SCRAM_MEMBERSHIP", "DIRECTORY.ORGANIZATION", "DIRECTORY.Z0_GRADE",
    "Stg_District", "Stg_School", "Stg_Student", "Stg_CourseMaster"
)

$schemas = [System.Collections.ArrayList]::new()

# Search repos for SQL files
Write-Host "Scanning repos for SQL table definitions..." -ForegroundColor Yellow
foreach ($repo in $Repos) {
    $repoPath = Join-Path $WorkspacePath $repo
    if (-not (Test-Path $repoPath)) {
        Write-Host "  Repo not found: $repo" -ForegroundColor Gray
        continue
    }

    Write-Host "  Scanning: $repo" -ForegroundColor Cyan
    
    # Find all .sql files
    $sqlFiles = Get-ChildItem -Path $repoPath -Filter "*.sql" -Recurse -ErrorAction SilentlyContinue
    
    foreach ($file in $sqlFiles) {
        try {
            $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
            if (-not $content) { continue }

            # Find CREATE TABLE statements
            $tableMatches = [regex]::Matches($content, "CREATE\s+TABLE\s+\[?([^\[\]\s]+)\]?\s*\[?([^\[\]\s]+)\]?\s*\(", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
            
            foreach ($tableMatch in $tableMatches) {
                $schema  = if ($tableMatch.Groups[1].Value -match "dbo|PSIS|Stg|Directory") { $tableMatch.Groups[1].Value } else { "dbo" }
                $table   = if ($tableMatch.Groups[2].Value) { $tableMatch.Groups[2].Value } else { $tableMatch.Groups[1].Value }
                
                $fullName = "$schema.$table"
                
                # Extract column definitions
                $tableStart = $tableMatch.Index
                $tableEnd   = $content.IndexOf(")", $tableStart)
                $tableDef   = $content.Substring($tableStart, $tableEnd - $tableStart + 1)
                
                # Simple column extraction (pattern: [ColumnName] DataType)
                $colMatches = [regex]::Matches($tableDef, "\[?(\w+)\]?\s+(VARCHAR|INT|DATETIME|CHAR|DECIMAL|SMALLINT|BIT|UNIQUEIDENTIFIER|TEXT|NVARCHAR|FLOAT)", [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
                
                $columns = @()
                foreach ($cm in $colMatches) {
                    $columns += [PSCustomObject]@{
                        ColumnName = $cm.Groups[1].Value
                        DataType   = $cm.Groups[2].Value
                    }
                }

                [void]$schemas.Add([PSCustomObject]@{
                    Repo           = $repo
                    SchemaTable    = $fullName
                    Schema         = $schema
                    TableName      = $table
                    ColumnCount    = $columns.Count
                    Columns        = ($columns.ColumnName -join "; ")
                    DataTypes      = ($columns.DataType -join "; ")
                    FilePath       = $file.FullName.Replace($WorkspacePath, "")
                    FileSize       = $file.Length
                })
            }
        }
        catch {
            Write-Verbose "Error processing $($file.FullName): $_"
        }
    }
}

$uniqueSchemas = $schemas | Group-Object SchemaTable | Select-Object @{ N="SchemaTable"; E={$_.Name} }, Count
Write-Host "Found $(@($schemas).Count) table definitions from $(@($uniqueSchemas).Count) unique tables" -ForegroundColor Green

# Filter to target tables only
Write-Host "Extracting target tables..." -ForegroundColor Yellow
$targetSchemas = @()
foreach ($target in $targetTables) {
    $targetSchemaMatch = $schemas | Where-Object { $_.SchemaTable -eq $target -or $_.TableName -eq $target }
    if ($targetSchemaMatch) {
        $targetSchemas += $targetSchemaMatch[0]
        Write-Host "  Found: $target" -ForegroundColor Green
    } else {
        Write-Host "  Missing: $target" -ForegroundColor Yellow
    }
}

Write-Host "`nExtracted $(($targetSchemas | Measure-Object).Count) target table schemas"  -ForegroundColor Green

# Export
$prefix = Join-Path $TracingFolder "database-schema-catalog"

foreach ($fmt in $Output) {
    if ($fmt -eq "CSV") {
        $out = "$prefix.csv"
        $schemas | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8
        Write-Host "CSV: $out" -ForegroundColor Green
    }
    if ($fmt -eq "JSON") {
        $out = "$prefix.json"
        $schemas | ConvertTo-Json -Depth 5 | Out-File -FilePath $out -Encoding UTF8
        Write-Host "JSON: $out" -ForegroundColor Green
    }
}

# Create summary of target tables
$summaryFile = Join-Path $TracingFolder "database-schema-summary.txt"
$targFound = $targetSchemas | Select-Object -ExpandProperty SchemaTable | Sort-Object -Unique | ForEach-Object { "  - $_" }
$targtargets = @()
foreach ($t in $targetTables) {
    if ($targetSchemas.SchemaTable -notcontains $t) { $targtargets += "  - $t" }
}
$repoSummary = $schemas | Group-Object Repo | ForEach-Object { "  $($_.Name): $($_.Count) tables" }

$summary = "Database Schema Catalog Summary`nGenerated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`n"
$summary += "`nTotal Tables Found: $(@($schemas).Count)`nTotal Target Tables: $(@($targetSchemas).Count)`n"
$summary += "`nTarget Tables with Definitions:`n"
$summary += ($targFound -join "`n") + "`n`n"
$summary += "Missing Target Tables:`n"
$summary += ($targtargets -join "`n") + "`n`n"
$summary += "Schema Summary by Repo:`n"
$summary += ($repoSummary -join "`n")

$summary | Out-File -FilePath $summaryFile -Encoding UTF8
Write-Host "Summary: $summaryFile" -ForegroundColor Green

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $TracingFolder `
    -SourceInputs @($PSCommandPath, $WorkspacePath) `
    -OutputPaths @(
        "$prefix.csv",
        "$prefix.json",
        $summaryFile
    )

Write-Host "`nSchema extraction complete!" -ForegroundColor Green
