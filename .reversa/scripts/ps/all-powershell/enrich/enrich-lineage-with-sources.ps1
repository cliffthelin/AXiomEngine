#Requires -Version 5.0
param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability",
    [string[]]$ExportFormats = @("CSV","JSON","HTML")
)

Write-Host "Report Lineage Enrichment Tool (v2)" -ForegroundColor Cyan

$lineageFile = Join-Path $TracingFolder "master-reports-output-lineage.json"
if (-not (Test-Path $lineageFile)) { Write-Error "Not found: $lineageFile"; exit 1 }

Write-Host "Loading lineage data..." -ForegroundColor Yellow
$lineageData = Get-Content -Path $lineageFile -Raw | ConvertFrom-Json
Write-Host "Loaded $(@($lineageData).Count) reports" -ForegroundColor Green

# --- Build lookup maps from journey table ---
# For each row, index by field name AND by any table.column reference found in any cell

$journeyFile = Join-Path $TracingFolder "field-crosswalk copy 2.md"
$sourceFamilyFile = Join-Path $TracingFolder "report-field-source-family.csv"
$sourceFamilyScript = Join-Path $TracingFolder "classify-report-source-family.ps1"
$buildFieldsFile = Join-Path $TracingFolder "master-reports-build-fields-by-field.csv"
$lineageCsvFile = Join-Path $TracingFolder "clearinghouse-to-report-lineage.csv"
Write-Host "Parsing journey table..." -ForegroundColor Yellow

$journeyByField  = @{}   # fieldName -> sourceInfo
$journeyByCol    = @{}   # "TABLE.COLUMN" (uppercase) -> sourceInfo

$upstreamObjectRules = @(
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.ORGANIZATION"
        UpstreamSource     = "CACTUS/RODS"
        Coverage           = "Confirmed operational feed"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.ORGANIZATION$"
        SourceEvidence     = "CactusSync schools flow validated against DIRECTORY.ORGANIZATION"
        Notes              = "CACTUS school and LEA synchronization feeds the organization reference path used by mixed-source report lineage."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.Z0_GRADE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.Z0_GRADE$"
        SourceEvidence     = "Database seed script Directory.Z0_GRADE_Data.sql"
        Notes              = "DIRECTORY.Z0_GRADE is populated by static INSERT seed data in the UTREx database project, not by CACTUS synchronization."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.STATE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.STATE$"
        SourceEvidence     = "Database seed script Directory.STATE_Data.sql"
        Notes              = "DIRECTORY.STATE is seeded from static reference inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.SCHOOL_TYPES"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.SCHOOL_TYPES$"
        SourceEvidence     = "Database seed script Directory.SCHOOL_TYPES_Data.sql"
        Notes              = "DIRECTORY.SCHOOL_TYPES is seeded from static lookup inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.ORGANIZATION_TYPE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.ORGANIZATION_TYPE$"
        SourceEvidence     = "Database seed script Directory.ORGANIZATION_TYPE_Data.sql"
        Notes              = "DIRECTORY.ORGANIZATION_TYPE is seeded from static hierarchy inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.LU_ETHNICITY"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.LU_ETHNICITY$"
        SourceEvidence     = "Database seed script Directory.LU_ETHNICITY_Data.sql"
        Notes              = "DIRECTORY.LU_ETHNICITY is seeded from static ethnicity lookup inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.RACE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.RACE$"
        SourceEvidence     = "Database seed script Directory.RACE_Data.sql"
        Notes              = "DIRECTORY.RACE is seeded from static race-code inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.LU_NEW_RACE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.LU_NEW_RACE$"
        SourceEvidence     = "Database seed script Directory.LU_NEW_RACE_Data.sql"
        Notes              = "DIRECTORY.LU_NEW_RACE is seeded from static race lookup inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.LU_REPORTING_RACE"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.LU_REPORTING_RACE$"
        SourceEvidence     = "Database seed script Directory.LU_REPORTING_RACE_Data.sql"
        Notes              = "DIRECTORY.LU_REPORTING_RACE is seeded from static reporting-race inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "DIRECTORY.ETH_RACE_DIM"
        UpstreamSource     = "Static Reference Data"
        Coverage           = "Confirmed seed data"
        Confidence         = "High"
        MatchingRule       = "^DIRECTORY\.ETH_RACE_DIM$"
        SourceEvidence     = "Database seed script Directory.ETH_RACE_DIM_Data.sql"
        Notes              = "DIRECTORY.ETH_RACE_DIM is seeded from static ethnicity-race dimension inserts in the UTREx database project."
    }
    [PSCustomObject]@{
        RuleScope          = "Object"
        MatchKey           = "PSIS.PSIS_COURSE_MASTER_STATE"
        UpstreamSource     = "CACTUS/RODS"
        Coverage           = "Much"
        Confidence         = "Medium"
        MatchingRule       = "^PSIS\.PSIS_COURSE_MASTER_STATE$"
        SourceEvidence     = "User-confirmed upstream lineage note"
        Notes              = "Much of the state course master is fed from CACTUS course-code data, so reports using this table should be treated as potentially CACTUS-fed."
    }
)

$sourceFamilyUpstreamRules = @(
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "UPASS/Fabric"; UpstreamSource = "UPASS/Fabric"; Coverage = "Direct family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found direct UPASS or Fabric evidence for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "Warehouse with UPASS path"; UpstreamSource = "Warehouse; UPASS/Fabric"; Coverage = "Mixed family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found warehouse objects plus UPASS/Fabric path evidence for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "UTREx with UPASS path"; UpstreamSource = "UPASS/Fabric"; Coverage = "Mixed family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found UTREx objects with downstream UPASS/Fabric path evidence for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "Data Warehouse"; UpstreamSource = "Warehouse"; Coverage = "Direct family tag"; Confidence = "Low"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found warehouse evidence without a narrower confirmed upstream source." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "DIBELS Warehouse"; UpstreamSource = "DIBELS Warehouse"; Coverage = "Direct family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found DIBELS warehouse evidence for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "Warehouse fed by UTREx"; UpstreamSource = "Warehouse; UTREx/PSIS"; Coverage = "Mixed family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found warehouse objects fed by UTREx production or staging lineage." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "Warehouse fed by CACTUS"; UpstreamSource = "Warehouse; CACTUS/RODS"; Coverage = "Mixed family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found warehouse objects fed by CACTUS lineage." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "Warehouse fed by UTREx and CACTUS"; UpstreamSource = "Warehouse; UTREx/PSIS; CACTUS/RODS"; Coverage = "Mixed family tag"; Confidence = "High"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found warehouse evidence with both UTREx and CACTUS lineage signals." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "UTREx/PSIS"; UpstreamSource = "UTREx/PSIS"; Coverage = "Direct family tag"; Confidence = "Low"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found direct UTREx or PSIS lineage for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "UTREx with CACTUS"; UpstreamSource = "UTREx/PSIS; CACTUS/RODS"; Coverage = "Mixed family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found UTREx objects with CACTUS-fed lineage signals for this report field." }
    [PSCustomObject]@{ RuleScope = "SourceFamily"; MatchKey = "CACTUS/RODS"; UpstreamSource = "CACTUS/RODS"; Coverage = "Direct family tag"; Confidence = "Medium"; SourceEvidence = "report-field-source-family.csv"; Notes = "Classifier found direct CACTUS lineage for this report field." }
)

$sourceFamilyByOutput = @{}

# Manual mapping: well-known PSIS production table columns -> SIF origin
# Columns in format "TABLE.COLUMN" -> SIF description
$knownMappings = @{
    "PSIS.GRADE_MEMBERSHIP.HISPANIC_FLAG"              = "StudentPersonal /PersonInfo/Demographics/RaceList (Ethnicity)"
    "PSIS.GRADE_MEMBERSHIP.NATIVE_AMERICAN_FLAG"       = "StudentPersonal /RaceList/Race[@Code='1005']"
    "PSIS.GRADE_MEMBERSHIP.ASIAN_FLAG"                 = "StudentPersonal /RaceList/Race[@Code='1002']"
    "PSIS.GRADE_MEMBERSHIP.BLACK_FLAG"                 = "StudentPersonal /RaceList/Race[@Code='1003']"
    "PSIS.GRADE_MEMBERSHIP.PACIFIC_ISLANDER_FLAG"      = "StudentPersonal /RaceList/Race[@Code='1004']"
    "PSIS.GRADE_MEMBERSHIP.WHITE_FLAG"                 = "StudentPersonal /RaceList/Race[@Code='1001']"
    "PSIS.GRADE_MEMBERSHIP.GRADE_ID"                   = "StudentSchoolEnrollment /GradeLevel/Code"
    "PSIS.GRADE_MEMBERSHIP.LIMITED_ENGLISH_ID"         = "StudentPersonal SIF_ExtendedElement UTExtensions/ELL"
    "PSIS.GRADE_MEMBERSHIP.FREE_RED_LUNCH_ID"          = "StudentParticipation /ProgramType[@Code='0819'] (EconomicDisadv)"
    "PSIS.GRADE_MEMBERSHIP.RESIDENT_STATUS_ID"         = "StudentPersonal SIF_ExtendedElement UTExtensions/ResidentStatus"
    "PSIS.GRADE_MEMBERSHIP.HOMELESS_ID"                = "StudentPersonal SIF_ExtendedElement UTExtensions/HomelessStatus"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.DISTRICT_STUDENT_ID"= "StudentPersonal /LocalId (StudentNumber)"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.SASID"              = "StudentPersonal /StateProvinceId (StatewideStudentID)"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.SSN"                = "StudentPersonal /PersonInfo/Demographics/SSN"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_LAST_NAME"   = "StudentPersonal /PersonInfo/Name/LastName"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_FIRST_NAME"  = "StudentPersonal /PersonInfo/Name/FirstName"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_MIDDLE_NAME" = "StudentPersonal /PersonInfo/Name/MiddleName"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.DATE_OF_BIRTH"      = "StudentPersonal /PersonInfo/Demographics/BirthDate"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.GENDER"             = "StudentPersonal /PersonInfo/Demographics/Sex"
    "PSIS.PSIS_DISTRICT_MEMBERSHIP.EXIT_TYPE_ID"       = "StudentSchoolEnrollment /ExitType/Code (ExitCode)"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.PRI_ORGANIZATION_ID" = "StudentSchoolEnrollment /SchoolInfoRefId (SchoolNumber)"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.ENTRY_DATE"          = "StudentSchoolEnrollment /EntryDate"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.EXIT_DATE"           = "StudentSchoolEnrollment /ExitDate"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.MEMBERSHIP_DAYS"     = "StudentAttendanceSummary /DaysInMembership (SchoolMembership)"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.ATTENDANCE_DAYS"     = "StudentAttendanceSummary /DaysAttended"
    "PSIS.PSIS_PRI_FAC_MEMBERSHIP.SCHOOL_OF_RECORD"    = "StudentSchoolEnrollment SIF_ExtendedElement UTExtensions/SchoolOfRecord"
    "PSIS.LU_EXIT_TYPE.EXIT_TYPE_DESC"                 = "Lookup: decoded from StudentSchoolEnrollment /ExitType/Code"
    "PSIS.LU_EXIT_TYPE.EXIT_TYPE_CODE"                 = "Lookup: decoded from StudentSchoolEnrollment /ExitType/Code"
    "PSIS.LU_LIMITED_ENGLISH.LIMITED_ENGLISH_DESC"     = "Lookup: decoded from StudentPersonal UTExtensions/ELL"
    "PSIS.LU_RESIDENT_STATUS.RESIDENT_STATUS_DESC"     = "Lookup: decoded from StudentPersonal UTExtensions/ResidentStatus"
    "PSIS.LU_FREE_RED_LUNCH.FREE_RED_LUNCH_DESC"       = "Lookup: decoded from StudentParticipation ProgramType EconomicDisadv"
    "PSIS.LU_HOMELESS.HOMELESS_DESC"                   = "Lookup: decoded from StudentPersonal UTExtensions/HomelessStatus"
    "PSIS.LU_HIGH_SCHOOL_COMPL_STATUS.HS_COMPL_DESC"   = "Lookup: decoded from StudentSchoolEnrollment/ExitType graduation"
    "PSIS.LU_SCRAM_DISABILITY_CODES.DISABILITY_DESC"   = "Lookup: decoded from StudentParticipation SPED disability code"
    "PSIS.LU_SCRAM_ENVIRONMENT_CODES.ENVIRONMENT_DESC" = "Lookup: decoded from StudentParticipation SPED environment code"
    "PSIS.LU_SCRAM_TIME_CODES.TIME_DESC"               = "Lookup: decoded from StudentParticipation SPED time code"
    "PSIS.LU_SCRAM_EXIT_CODES.EXIT_DESC"               = "Lookup: decoded from StudentParticipation SPED exit code"
    "PSIS.LU_YIC_TIME_CODES.YIC_TIME_DESC"             = "Lookup: decoded from StudentParticipation YIC time code"
    "PSIS.LU_KINDERGARTEN_TYPES.KINDER_DESC"           = "Lookup: decoded from StudentPersonal kindergarten indicator"
    "PSIS.LU_PART_TIME_HOMESCHOOL.HOMESCHOOL_DESC"     = "Lookup: decoded from StudentSchoolEnrollment HomeSchooledStudent"
    "PSIS.PSIS_SCRAM_MEMBERSHIP.DISABILITY_CODE"       = "StudentParticipation SPED disability payload"
    "DIRECTORY.ORGANIZATION.ORGANIZATION_ID"           = "LEAInfo /LocalId or SchoolInfo /LocalId"
    "DIRECTORY.ORGANIZATION.DISTRICT_NUMBER"           = "LEAInfo /LocalId (LeaNumber)"
    "DIRECTORY.ORGANIZATION.SCHOOL_NUMBER"             = "SchoolInfo /LocalId (SchoolNumber)"
    "DIRECTORY.ORGANIZATION.ORG_NAME"                  = "LEAInfo or SchoolInfo /Name"
    "DIRECTORY.Z0_GRADE.GRADE_CODE"                    = "StudentSchoolEnrollment /GradeLevel/Code"
    "DIRECTORY.Z0_GRADE.GRADE_DESC"                    = "Lookup: decoded from StudentSchoolEnrollment /GradeLevel/Code"
}

if (Test-Path $journeyFile) {
    $lines   = Get-Content -Path $journeyFile -Encoding UTF8
    $inTable = $false

    foreach ($line in $lines) {
        if ($line -match "^# Unified End-to-End Field Journey Table") { $inTable = $true; continue }
        if (-not $inTable) { continue }
        if ($line -notmatch "^\|") { continue }
        if ($line -match "^[\| \-]+$") { continue }

        $cells = ($line -split "\|") | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
        if ($cells.Count -lt 4) { continue }

        $fieldName = $cells[2]
        $sifPath   = $cells[3]

        # Index by field name
        if ($fieldName -and -not $journeyByField.ContainsKey($fieldName)) {
            $journeyByField[$fieldName] = @{
                SIFObject = $sifPath
                STGTable  = if ($cells.Count -gt 4) { $cells[4] } else { "" }
                PSISInfo  = if ($cells.Count -gt 5) { $cells[5] } else { "" }
            }
        }

        # Index every TABLE.COLUMN pattern found anywhere in the row
        foreach ($cell in $cells) {
            $matches2 = [regex]::Matches($cell, "(PSIS\.(?:Stg_|LU_|PSIS_)?[A-Za-z_]+|DIRECTORY\.[A-Za-z_0-9]+)\.([A-Za-z_]+)")
            foreach ($m in $matches2) {
                $key = "$($m.Groups[1].Value.ToUpper()).$($m.Groups[2].Value.ToUpper())"
                if (-not $journeyByCol.ContainsKey($key)) {
                    $journeyByCol[$key] = @{ SIFObject=$sifPath; FieldName=$fieldName }
                }
            }
        }
    }
    Write-Host "Journey: $($journeyByField.Count) field entries, $($journeyByCol.Count) table.column entries" -ForegroundColor Green
}

# Add known manual mappings into the lookup
foreach ($k in $knownMappings.Keys) {
    if (-not $journeyByCol.ContainsKey($k)) {
        $journeyByCol[$k] = @{ SIFObject=$knownMappings[$k]; FieldName="(manual mapping)" }
    }
}
Write-Host "Total table.column lookups (incl. manual): $($journeyByCol.Count)" -ForegroundColor Cyan

function Get-TableColumns {
    param([object]$Node, [System.Collections.ArrayList]$Out)
    if (-not $Node) { return }
    if ($Node.node_type -eq "table_column" -and $Node.column) {
        [void]$Out.Add([PSCustomObject]@{ Table=$Node.table; Column=$Node.column })
    }
    foreach ($c in $Node.children) { Get-TableColumns -Node $c -Out $Out }
}

function Get-ParentFields {
    param([object]$Node)

    $parents = [System.Collections.ArrayList]::new()
    if (-not $Node) { return "" }

    foreach ($sqlObject in @($Node.children)) {
        if ($sqlObject.node_type -ne "sql_object") { continue }
        foreach ($sqlDefinition in @($sqlObject.children)) {
            if ($sqlDefinition.node_type -ne "sql_definition") { continue }

            $definitionRefs = [System.Collections.ArrayList]::new()
            foreach ($child in @($sqlDefinition.children)) {
                Get-TableColumns -Node $child -Out $definitionRefs
            }

            foreach ($ref in $definitionRefs) {
                $parentName = if ($ref.Table) { "$($ref.Table).$($ref.Column)" } else { $ref.Column }
                if (-not [string]::IsNullOrWhiteSpace($parentName) -and $parents -notcontains $parentName) {
                    [void]$parents.Add($parentName)
                }
            }
        }
    }

    return ($parents -join "; ")
}

function Join-UniqueValues {
    param([string[]]$Values)

    @($Values | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Select-Object -Unique) -join "; "
}

function Invoke-SourceFamilyClassifier {
    param([string]$Reason)

    if (-not (Test-Path $sourceFamilyScript)) {
        Write-Warning "Source-family classifier not found: $sourceFamilyScript"
        return
    }

    Write-Host "Refreshing source-family artifact ($Reason)..." -ForegroundColor Yellow
    & $sourceFamilyScript -TracingFolder $TracingFolder -ExportFormats @("CSV", "JSON")
}

function Ensure-SourceFamilyArtifact {
    $shouldRefresh = -not (Test-Path $sourceFamilyFile)

    if (-not $shouldRefresh) {
        $sourceFamilyTimestamp = (Get-Item $sourceFamilyFile).LastWriteTimeUtc
        $dependencyPaths = @($sourceFamilyScript, $buildFieldsFile, $journeyFile, $lineageCsvFile)
        foreach ($dependencyPath in $dependencyPaths) {
            if ((Test-Path $dependencyPath) -and ((Get-Item $dependencyPath).LastWriteTimeUtc -gt $sourceFamilyTimestamp)) {
                $shouldRefresh = $true
                break
            }
        }
    }

    if ($shouldRefresh) {
        $reason = if (Test-Path $sourceFamilyFile) { "dependency changed" } else { "artifact missing" }
        Invoke-SourceFamilyClassifier -Reason $reason
    }
}

function Get-HighestConfidence {
    param([string[]]$ConfidenceValues)

    if ($ConfidenceValues -contains "High") { return "High" }
    if ($ConfidenceValues -contains "Medium") { return "Medium" }
    if ($ConfidenceValues -contains "Low") { return "Low" }
    return ""
}

function Get-ObjectRuleUpstreamInfo {
    param(
        [System.Collections.ArrayList]$Refs,
        [object[]]$RuleMap
    )

    $tables = @($Refs | Where-Object { $_.Table } | ForEach-Object { $_.Table.ToUpper() } | Select-Object -Unique)
    $matchedRules = @()

    foreach ($rule in $RuleMap) {
        $matchedTables = @($tables | Where-Object { $_ -match $rule.MatchingRule })
        if ($matchedTables.Count -gt 0) {
            $matchedRules += [PSCustomObject]@{
                Rule   = $rule
                Tables = $matchedTables
            }
        }
    }

    if ($matchedRules.Count -eq 0) {
        return [PSCustomObject]@{
            PotentialUpstreamSource     = ""
            PotentialUpstreamConfidence = ""
            PotentialUpstreamObjects    = ""
            PotentialUpstreamReason     = ""
            PotentialUpstreamEvidence   = ""
        }
    }

    return [PSCustomObject]@{
        PotentialUpstreamSource     = Join-UniqueValues -Values @($matchedRules | ForEach-Object { $_.Rule.UpstreamSource })
        PotentialUpstreamConfidence = Get-HighestConfidence -ConfidenceValues @($matchedRules | ForEach-Object { $_.Rule.Confidence })
        PotentialUpstreamObjects    = Join-UniqueValues -Values @($matchedRules | ForEach-Object { $_.Tables })
        PotentialUpstreamReason     = Join-UniqueValues -Values @($matchedRules | ForEach-Object { $_.Rule.Notes })
        PotentialUpstreamEvidence   = Join-UniqueValues -Values @($matchedRules | ForEach-Object { $_.Rule.SourceEvidence })
    }
}

function Get-SourceFamilyUpstreamInfo {
    param(
        [string]$ReportTag,
        [string]$OutputField,
        [System.Collections.ArrayList]$Refs,
        [hashtable]$SourceFamilyLookup,
        [object[]]$RuleMap
    )

    $lookupKey = "{0}|{1}" -f $ReportTag, $OutputField
    if (-not $SourceFamilyLookup.ContainsKey($lookupKey)) {
        return [PSCustomObject]@{
            PotentialUpstreamSource     = ""
            PotentialUpstreamConfidence = ""
            PotentialUpstreamObjects    = ""
            PotentialUpstreamReason     = ""
            PotentialUpstreamEvidence   = ""
        }
    }

    $sourceFamilyRow = $SourceFamilyLookup[$lookupKey]
    $matchedRule = $RuleMap | Where-Object { $_.MatchKey -eq $sourceFamilyRow.SourceFamily } | Select-Object -First 1
    if (-not $matchedRule) {
        return [PSCustomObject]@{
            PotentialUpstreamSource     = ""
            PotentialUpstreamConfidence = ""
            PotentialUpstreamObjects    = ""
            PotentialUpstreamReason     = ""
            PotentialUpstreamEvidence   = ""
        }
    }

    $tables = @($Refs | Where-Object { $_.Table } | ForEach-Object { $_.Table.ToUpper() } | Select-Object -Unique)
    if ($tables.Count -eq 0 -and -not [string]::IsNullOrWhiteSpace($sourceFamilyRow.IntermediateFields)) {
        $tables = @(([regex]::Matches($sourceFamilyRow.IntermediateFields, '(?i)([A-Za-z0-9_]+\.[A-Za-z0-9_]+)')) | ForEach-Object { $_.Groups[1].Value.ToUpper() } | Select-Object -Unique)
    }

    return [PSCustomObject]@{
        PotentialUpstreamSource     = $matchedRule.UpstreamSource
        PotentialUpstreamConfidence = Get-HighestConfidence -ConfidenceValues @($sourceFamilyRow.Confidence, $matchedRule.Confidence)
        PotentialUpstreamObjects    = Join-UniqueValues -Values $tables
        PotentialUpstreamReason     = Join-UniqueValues -Values @($matchedRule.Notes, $sourceFamilyRow.NextTraceTarget)
        PotentialUpstreamEvidence   = Join-UniqueValues -Values @($matchedRule.SourceEvidence, $sourceFamilyRow.EvidenceTags)
    }
}

function Get-PotentialUpstreamInfo {
    param(
        [string]$ReportTag,
        [string]$OutputField,
        [System.Collections.ArrayList]$Refs,
        [hashtable]$SourceFamilyLookup,
        [object[]]$ObjectRuleMap,
        [object[]]$SourceFamilyRuleMap
    )

    $objectInfo = Get-ObjectRuleUpstreamInfo -Refs $Refs -RuleMap $ObjectRuleMap
    if ($objectInfo.PotentialUpstreamSource) {
        return $objectInfo
    }

    return Get-SourceFamilyUpstreamInfo -ReportTag $ReportTag -OutputField $OutputField -Refs $Refs -SourceFamilyLookup $SourceFamilyLookup -RuleMap $SourceFamilyRuleMap
}

Ensure-SourceFamilyArtifact

if (Test-Path $sourceFamilyFile) {
    $sourceFamilyRows = Import-Csv -Path $sourceFamilyFile
    foreach ($row in $sourceFamilyRows) {
        $key = "{0}|{1}" -f $row.ReportTag, $row.OutputField
        if (-not $sourceFamilyByOutput.ContainsKey($key)) {
            $sourceFamilyByOutput[$key] = $row
        }
    }
    Write-Host "Source-family classifier rows: $($sourceFamilyByOutput.Count)" -ForegroundColor Green
}

Write-Host "Enriching lineage..." -ForegroundColor Yellow
$enriched            = [System.Collections.ArrayList]::new()
$fieldCount          = 0
$matchedDirect       = 0
$matchedProd         = 0
$matchedManual       = 0
$notFound            = 0
$upstreamTagged      = 0

foreach ($report in $lineageData) {
    foreach ($fl in $report.output_field_lineage) {
        $fn      = $fl.field_name
        $refs    = [System.Collections.ArrayList]::new()
        Get-TableColumns -Node $fl.lineage_tree -Out $refs
        $parentFields = Get-ParentFields -Node $fl.lineage_tree

        $srcType  = "Not Found"
        $srcSIF   = "Not Found"
        $srcStg   = ""
        $srcProd  = ""

        # 1. Direct field name match in journey table
        if ($journeyByField.ContainsKey($fn)) {
            $m = $journeyByField[$fn]
            $srcType = "Direct"
            $srcSIF  = $m.SIFObject
            $srcStg  = $m.STGTable
            $srcProd = $m.PSISInfo
            $matchedDirect++
        } else {
            # 2. Match via TABLE.COLUMN reference in lineage tree
            foreach ($r in $refs) {
                $key = "$($r.Table.ToUpper()).$($r.Column.ToUpper())"
                if ($journeyByCol.ContainsKey($key)) {
                    $m = $journeyByCol[$key]
                    $srcSIF  = $m.SIFObject
                    if ($knownMappings.ContainsKey($key)) {
                        $srcType = "Via Lookup/Prod Table"
                        $matchedManual++
                    } else {
                        $srcType = "Via STG/PSIS Column"
                        $matchedProd++
                    }
                    break
                }
            }
            if ($srcType -eq "Not Found") { $notFound++ }
        }

        $iFields = ($refs | ForEach-Object { "$($_.Table).$($_.Column)" } | Select-Object -Unique) -join "; "
        $upstreamInfo = Get-PotentialUpstreamInfo -ReportTag $report.report_tag -OutputField $fn -Refs $refs -SourceFamilyLookup $sourceFamilyByOutput -ObjectRuleMap $upstreamObjectRules -SourceFamilyRuleMap $sourceFamilyUpstreamRules
        if ($upstreamInfo.PotentialUpstreamSource) { $upstreamTagged++ }

        [void]$enriched.Add([PSCustomObject]@{
            ReportTag              = $report.report_tag
            ReportName             = $report.friendly_name
            OutputField            = $fn
            SourceType             = $srcType
            ClearinghouseSIFObject = $srcSIF
            STGTable               = $srcStg
            PSISProductionInfo     = $srcProd
            ParentTableFields      = $parentFields
            IntermediateFields     = $iFields
            PotentialUpstreamSource = $upstreamInfo.PotentialUpstreamSource
            PotentialUpstreamConfidence = $upstreamInfo.PotentialUpstreamConfidence
            PotentialUpstreamObjects = $upstreamInfo.PotentialUpstreamObjects
            PotentialUpstreamReason = $upstreamInfo.PotentialUpstreamReason
            PotentialUpstreamEvidence = $upstreamInfo.PotentialUpstreamEvidence
        })
        $fieldCount++
    }
}

Write-Host "Enriched $fieldCount field lineages:" -ForegroundColor Green
Write-Host "  Direct (field name match)    : $matchedDirect" -ForegroundColor Cyan
Write-Host "  Via STG/PSIS column match    : $matchedProd" -ForegroundColor Cyan
Write-Host "  Via Lookup/Production tables : $matchedManual" -ForegroundColor Cyan
Write-Host "  Not traced                   : $notFound" -ForegroundColor Yellow
Write-Host "  Tagged with upstream rules   : $upstreamTagged" -ForegroundColor Cyan
$traced = $matchedDirect + $matchedProd + $matchedManual
$pct    = if ($fieldCount -gt 0) { [math]::Round($traced/$fieldCount*100, 1) } else { 0 }
Write-Host "  Total traced                 : $traced ($pct%)" -ForegroundColor Green

$prefix = Join-Path $TracingFolder "clearinghouse-to-report-lineage"
$upstreamRules = @($upstreamObjectRules + $sourceFamilyUpstreamRules)
$upstreamRulesPrefix = Join-Path $TracingFolder "upstream-source-rules"

foreach ($fmt in $ExportFormats) {
    if ($fmt -eq "CSV") {
        $out = "$prefix.csv"
        $enriched | Export-Csv -Path $out -NoTypeInformation -Encoding UTF8
        Write-Host "CSV: $out" -ForegroundColor Green

        Invoke-SourceFamilyClassifier -Reason "lineage export regenerated"

        $mapOut = "$upstreamRulesPrefix.csv"
        $upstreamRules | Export-Csv -Path $mapOut -NoTypeInformation -Encoding UTF8
        Write-Host "CSV: $mapOut" -ForegroundColor Green
    }
    if ($fmt -eq "JSON") {
        $out = "$prefix.json"
        $enriched | ConvertTo-Json -Depth 5 | Out-File -FilePath $out -Encoding UTF8
        Write-Host "JSON: $out" -ForegroundColor Green

        $mapOut = "$upstreamRulesPrefix.json"
        $upstreamRules | ConvertTo-Json -Depth 5 | Out-File -FilePath $mapOut -Encoding UTF8
        Write-Host "JSON: $mapOut" -ForegroundColor Green
    }
    if ($fmt -eq "HTML") {
        $out = "$prefix.html"
        $rows = foreach ($row in $enriched | Sort-Object ReportTag, OutputField) {
            $cls = switch -Wildcard ($row.SourceType) {
                "Direct"   { "d" }
                "Via *"    { "i" }
                default    { "n" }
            }
            "<tr class='$cls'><td>$($row.ReportTag)</td><td><b>$($row.OutputField)</b></td>" +
            "<td>$($row.SourceType)</td><td>$($row.ClearinghouseSIFObject)</td>" +
            "<td>$($row.STGTable)</td><td>$($row.PSISProductionInfo)</td>" +
            "<td><small>$($row.ParentTableFields)</small></td>" +
            "<td>$($row.PotentialUpstreamSource)</td><td>$($row.PotentialUpstreamConfidence)</td>" +
            "<td><small>$($row.PotentialUpstreamObjects)</small></td>" +
            "<td><small>$($row.IntermediateFields)</small></td></tr>"
        }
        $html = "<!DOCTYPE html><html><head><title>Clearinghouse to Report Lineage v3</title><style>" +
            "body{font-family:Arial,sans-serif;margin:20px;font-size:13px}" +
            "table{border-collapse:collapse;width:100%}" +
            "th,td{border:1px solid #ccc;padding:5px 8px}th{background:#2e6da4;color:#fff;position:sticky;top:0}" +
            "tr.d{background:#dff0d8}tr.i{background:#fcf8e3}tr.n{background:#f2dede}" +
            ".sum{background:#d9edf7;padding:10px;margin:10px 0;border-radius:4px;font-size:14px}" +
            "h2{margin-bottom:4px}" +
            "</style></head><body>" +
            "<h2>Clearinghouse to Report Field Lineage</h2>" +
            "<div class='sum'>" +
            "<b>Fields traced:</b> $fieldCount &nbsp;|&nbsp;" +
            "<b>Direct from SIF:</b> $matchedDirect &nbsp;|&nbsp;" +
            "<b>Via STG/PSIS column:</b> $matchedProd &nbsp;|&nbsp;" +
            "<b>Via Lookup/Prod tables:</b> $matchedManual &nbsp;|&nbsp;" +
            "<b>Tagged with upstream rules:</b> $upstreamTagged &nbsp;|&nbsp;" +
            "<b>Not traced:</b> $notFound &nbsp;|&nbsp;" +
            "<b>Coverage:</b> $pct% &nbsp;| Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')" +
            "</div>" +
            "<table><tr><th>Report</th><th>Output Field</th><th>Lineage Type</th>" +
            "<th>Clearinghouse SIF Object / Path</th><th>STG Table/Field</th><th>PSIS Production</th><th>Parent Table.Fields</th><th>Potential Upstream Source</th><th>Upstream Confidence</th><th>Upstream Objects</th>" +
            "<th>Intermediate DB Tables/Fields</th></tr>" +
            ($rows -join "") +
            "</table><p><small>Green=direct SIF input | Yellow=traced via column/lookup match | Red=source not yet traced</small></p>" +
            "</body></html>"
        $html | Out-File -FilePath $out -Encoding UTF8
        Write-Host "HTML: $out" -ForegroundColor Green
    }
}

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource $TracingFolder `
    -SourceInputs @($PSCommandPath, $lineageFile, $journeyFile, $buildFieldsFile, $sourceFamilyScript) `
    -OutputPaths @(
        $lineageCsvFile,
        ([System.IO.Path]::ChangeExtension($lineageCsvFile, 'json')),
        ([System.IO.Path]::ChangeExtension($lineageCsvFile, 'html')),
        (Join-Path $TracingFolder 'report-field-source-family.csv'),
        (Join-Path $TracingFolder 'report-field-source-family.json'),
        "$upstreamRulesPrefix.csv",
        "$upstreamRulesPrefix.json"
    )

Write-Host "`nSource type breakdown:" -ForegroundColor Cyan
$enriched | Group-Object SourceType | Sort-Object Count -Descending | Format-Table Name,Count -AutoSize

Write-Host "Top Clearinghouse SIF objects referenced across all reports:" -ForegroundColor Cyan
$enriched | Where-Object { $_.ClearinghouseSIFObject -ne "Not Found" } |
    Group-Object ClearinghouseSIFObject | Sort-Object Count -Descending | Select-Object -First 20 |
    Format-Table Name,Count -AutoSize

Write-Host "Done." -ForegroundColor Green
