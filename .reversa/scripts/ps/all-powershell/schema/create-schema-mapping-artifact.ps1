#Requires -Version 5.0
<#
.SYNOPSIS
Creates a database schema mapping artifact for PSIS and Directory tables based on SQL usage patterns.

.DESCRIPTION
Maps PSIS production tables and columns back to their Clearinghouse SIF origins.
Data sourced from:
- Observed SQL queries in lineage (field usage)
- Migration scripts showing ETL logic
- C# models in FinalizerService-develop
- Published schema documentation

.EXAMPLE
.\create-schema-mapping-artifact.ps1
#>

param(
    [string]$TracingFolder = "c:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability"
)

Write-Host "Creating Database Schema Mapping Artifact" -ForegroundColor Cyan

# Define known PSIS tables and their columns with Clearinghouse source mapping
$schemaMapping = @(
    # PSIS.PSIS_DISTRICT_MEMBERSHIP - top-level student identity record
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "DISTRICT_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = "Generated key"; ClearinghouseObject = "StudentPersonal/LocalId"; Notes = "PK" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "DISTRICT_STUDENT_ID"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/LocalId"; ClearinghouseObject = "S1"; Notes = "LEA-assigned ID" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "SASID"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/StateProvinceId"; ClearinghouseObject = "S1"; Notes = "Statewide unique ID" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "SSN"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/SSN"; ClearinghouseObject = "S1"; Notes = "Highly restricted" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "FORMAL_FIRST_NAME"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Name/FirstName"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "FORMAL_LAST_NAME"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Name/LastName"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "FORMAL_MIDDLE_NAME"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Name/MiddleName"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "DATE_OF_BIRTH"; 
       DataType = "DATETIME"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/BirthDate"; ClearinghouseObject = "S1"; Notes = "PII" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "GENDER"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/Sex"; ClearinghouseObject = "S1"; Notes = "M/F code" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "EXIT_TYPE_ID"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/ExitType/Code"; ClearinghouseObject = "S1"; Notes = "FK → LU_EXIT_TYPE" }
    @{ Table = "PSIS.PSIS_DISTRICT_MEMBERSHIP"; Column = "REPORTING_ORGANIZATION_ID"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "LEAInfo/LocalId"; ClearinghouseObject = "DI"; Notes = "FK → DIRECTORY.ORGANIZATION" }
    
    # PSIS.PSIS_PRI_FAC_MEMBERSHIP - primary facility (school) enrollment
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "PRI_FAC_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = "Generated key"; ClearinghouseObject = ""; Notes = "PK" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "DISTRICT_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = ""; ClearinghouseObject = ""; Notes = "FK → PSIS_DISTRICT_MEMBERSHIP" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "PRI_ORGANIZATION_ID"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "SchoolInfo/LocalId"; ClearinghouseObject = "SC"; Notes = "FK → DIRECTORY.ORGANIZATION" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "ENTRY_DATE"; 
       DataType = "DATETIME"; ClearinghouseSource = "StudentSchoolEnrollment/EntryDate"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "EXIT_DATE"; 
       DataType = "DATETIME"; ClearinghouseSource = "StudentSchoolEnrollment/ExitDate"; ClearinghouseObject = "S1"; Notes = "Vendor off-by-one quirk" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "MEMBERSHIP_DAYS"; 
       DataType = "INT"; ClearinghouseSource = "StudentAttendanceSummary/DaysInMembership"; ClearinghouseObject = "S1"; Notes = "Calculated" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "ATTENDANCE_DAYS"; 
       DataType = "INT"; ClearinghouseSource = "StudentAttendanceSummary/DaysAttended"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.PSIS_PRI_FAC_MEMBERSHIP"; Column = "SCHOOL_OF_RECORD"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentSchoolEnrollment/SIF_ExtendedElement/UTExtensions/SchoolOfRecord"; ClearinghouseObject = "S1"; Notes = "UTExtensions" }
    
    # PSIS.GRADE_MEMBERSHIP - grade-level enrollment and demographics
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "GRADE_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = "Generated key"; ClearinghouseObject = ""; Notes = "PK" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "PRI_FAC_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = ""; ClearinghouseObject = ""; Notes = "FK → PSIS_PRI_FAC_MEMBERSHIP" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "GRADE_ID"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/GradeLevel/Code"; ClearinghouseObject = "S1"; Notes = "FK → DIRECTORY.Z0_GRADE" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "SCHOOL_YEAR"; 
       DataType = "SMALLINT"; ClearinghouseSource = "manifest property Vrf.Property.CurrentSchoolYear"; ClearinghouseObject = "DI"; Notes = "" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "MEMBERSHIP_DAYS"; 
       DataType = "INT"; ClearinghouseSource = "StudentAttendanceSummary/DaysInMembership"; ClearinghouseObject = "S1"; Notes = "Derived from PSIS_PRI_FAC" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "ATTENDANCE_DAYS"; 
       DataType = "INT"; ClearinghouseSource = "StudentAttendanceSummary/DaysAttended"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "HISPANIC_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='H']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "NATIVE_AMERICAN_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='1005']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "ASIAN_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='1002']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "BLACK_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='1003']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "PACIFIC_ISLANDER_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='1004']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "WHITE_FLAG"; 
       DataType = "VARCHAR(1)"; ClearinghouseSource = "StudentPersonal/PersonInfo/Demographics/RaceList/Race[@Code='1001']"; ClearinghouseObject = "S1"; Notes = "Y/N" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "FREE_RED_LUNCH_ID"; 
       DataType = "INT"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='0819']"; ClearinghouseObject = "S1"; Notes = "FK → LU_FREE_RED_LUNCH" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "LIMITED_ENGLISH_ID"; 
       DataType = "INT"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/ELL"; ClearinghouseObject = "S1"; Notes = "FK → LU_LIMITED_ENGLISH; UTExtensions" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "RESIDENT_STATUS_ID"; 
       DataType = "INT"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/ResidentStatus"; ClearinghouseObject = "S1"; Notes = "FK → LU_RESIDENT_STATUS; UTExtensions" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "HOMELESS_ID"; 
       DataType = "INT"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/HomelessStatus"; ClearinghouseObject = "S1"; Notes = "FK → LU_HOMELESS; UTExtensions" }
    @{ Table = "PSIS.GRADE_MEMBERSHIP"; Column = "ENG_LANG_LEARNER"; 
       DataType = "INT"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/ELL"; ClearinghouseObject = "S1"; Notes = "Direct flag, derived from LIMITED_ENGLISH_ID" }
    
    # PSIS.PSIS_SCRAM_MEMBERSHIP - special education (SCRAM = Special Circumstances Related to Academic Movement)
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "SCRAM_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = "Generated key"; ClearinghouseObject = ""; Notes = "PK" }
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "GRADE_MEMBERSHIP_ID"; 
       DataType = "INT"; ClearinghouseSource = ""; ClearinghouseObject = ""; Notes = "FK → GRADE_MEMBERSHIP" }
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "DISABILITY_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/DisabilityCode"; ClearinghouseObject = "S2"; Notes = "FK → LU_SCRAM_DISABILITY_CODES" }
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "ENVIRONMENT_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/EnvironmentCode"; ClearinghouseObject = "S2"; Notes = "FK → LU_SCRAM_ENVIRONMENT_CODES" }
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "TIME_IN_GEN_ED"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/TimeInGeneralEducation"; ClearinghouseObject = "S2"; Notes = "FK → LU_SCRAM_TIME_CODES" }
    @{ Table = "PSIS.PSIS_SCRAM_MEMBERSHIP"; Column = "EXIT_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/ExitCode"; ClearinghouseObject = "S2"; Notes = "FK → LU_SCRAM_EXIT_CODES" }
    
    # PSIS Lookup Tables
    @{ Table = "PSIS.LU_EXIT_TYPE"; Column = "EXIT_TYPE_ID"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "FK from PSIS_DISTRICT_MEMBERSHIP.EXIT_TYPE_ID" }
    @{ Table = "PSIS.LU_EXIT_TYPE"; Column = "EXIT_TYPE_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/ExitType/Code"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.LU_EXIT_TYPE"; Column = "EXIT_TYPE_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentSchoolEnrollment/ExitType/Description"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.LU_LIMITED_ENGLISH"; Column = "LIMITED_ENGLISH_ID"; 
       DataType = "INT"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "FK from GRADE_MEMBERSHIP.LIMITED_ENGLISH_ID" }
    @{ Table = "PSIS.LU_LIMITED_ENGLISH"; Column = "CODE"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/ELL"; ClearinghouseObject = "S1"; Notes = "UTExtensions" }
    @{ Table = "PSIS.LU_LIMITED_ENGLISH"; Column = "DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_RESIDENT_STATUS"; Column = "RESIDENT_STATUS_ID"; 
       DataType = "INT"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "FK from GRADE_MEMBERSHIP.RESIDENT_STATUS_ID" }
    @{ Table = "PSIS.LU_RESIDENT_STATUS"; Column = "CODE"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/ResidentStatus"; ClearinghouseObject = "S1"; Notes = "UTExtensions" }
    @{ Table = "PSIS.LU_RESIDENT_STATUS"; Column = "DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_FREE_RED_LUNCH"; Column = "FREE_RED_LUNCH_ID"; 
       DataType = "INT"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "FK from GRADE_MEMBERSHIP.FREE_RED_LUNCH_ID" }
    @{ Table = "PSIS.LU_FREE_RED_LUNCH"; Column = "CODE"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='0819']"; ClearinghouseObject = "S1"; Notes = "EconomicDisadv" }
    @{ Table = "PSIS.LU_FREE_RED_LUNCH"; Column = "DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_HOMELESS"; Column = "HOMELESS_ID"; 
       DataType = "INT"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "FK from GRADE_MEMBERSHIP.HOMELESS_ID" }
    @{ Table = "PSIS.LU_HOMELESS"; Column = "CODE"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions/HomelessStatus"; ClearinghouseObject = "S1"; Notes = "UTExtensions" }
    @{ Table = "PSIS.LU_HOMELESS"; Column = "DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_HIGH_SCHOOL_COMPL_STATUS"; Column = "HS_COMPL_ID"; 
       DataType = "INT"; ClearinghouseSource = "Lookup"; ClearinghouseObject = ""; Notes = "Graduation status" }
    @{ Table = "PSIS.LU_HIGH_SCHOOL_COMPL_STATUS"; Column = "CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/ExitType/Code (graduation codes)"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.LU_HIGH_SCHOOL_COMPL_STATUS"; Column = "DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentSchoolEnrollment/ExitType/Description"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_DISABILITY_CODES"; Column = "DISABILITY_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/DisabilityCode"; ClearinghouseObject = "S2"; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_DISABILITY_CODES"; Column = "DISABILITY_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_ENVIRONMENT_CODES"; Column = "ENVIRONMENT_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/EnvironmentCode"; ClearinghouseObject = "S2"; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_ENVIRONMENT_CODES"; Column = "ENVIRONMENT_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_TIME_CODES"; Column = "TIME_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/TimeInGeneralEducation"; ClearinghouseObject = "S2"; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_TIME_CODES"; Column = "TIME_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_EXIT_CODES"; Column = "EXIT_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentParticipation/ProgramType[@Code='SPED']/ExitCode"; ClearinghouseObject = "S2"; Notes = "" }
    @{ Table = "PSIS.LU_SCRAM_EXIT_CODES"; Column = "EXIT_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_KINDERGARTEN_TYPES"; Column = "KINDER_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentPersonal/SIF_ExtendedElement/UTExtensions (kindergarten indicator)"; ClearinghouseObject = "S1"; Notes = "UTExtensions" }
    @{ Table = "PSIS.LU_KINDERGARTEN_TYPES"; Column = "KINDER_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    @{ Table = "PSIS.LU_PART_TIME_HOMESCHOOL"; Column = "HOMESCHOOL_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/HomeSchooledStudent"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "PSIS.LU_PART_TIME_HOMESCHOOL"; Column = "HOMESCHOOL_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "Lookup description"; ClearinghouseObject = ""; Notes = "" }
    
    # Directory Reference Tables
    @{ Table = "DIRECTORY.ORGANIZATION"; Column = "ORGANIZATION_ID"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "LEAInfo/LocalId or SchoolInfo/LocalId"; ClearinghouseObject = "DI/SC"; Notes = "PK: LEA or School ID" }
    @{ Table = "DIRECTORY.ORGANIZATION"; Column = "DISTRICT_NUMBER"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "LEAInfo/LocalId"; ClearinghouseObject = "DI"; Notes = "LEA number" }
    @{ Table = "DIRECTORY.ORGANIZATION"; Column = "SCHOOL_NUMBER"; 
       DataType = "VARCHAR(50)"; ClearinghouseSource = "SchoolInfo/LocalId"; ClearinghouseObject = "SC"; Notes = "School number" }
    @{ Table = "DIRECTORY.ORGANIZATION"; Column = "ORG_NAME"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "LEAInfo/Name or SchoolInfo/Name"; ClearinghouseObject = "DI/SC"; Notes = "" }
    @{ Table = "DIRECTORY.Z0_GRADE"; Column = "GRADE_ID"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/GradeLevel/Code"; ClearinghouseObject = "S1"; Notes = "FK from GRADE_MEMBERSHIP.GRADE_ID" }
    @{ Table = "DIRECTORY.Z0_GRADE"; Column = "GRADE_CODE"; 
       DataType = "VARCHAR(10)"; ClearinghouseSource = "StudentSchoolEnrollment/GradeLevel/Code"; ClearinghouseObject = "S1"; Notes = "" }
    @{ Table = "DIRECTORY.Z0_GRADE"; Column = "GRADE_DESC"; 
       DataType = "VARCHAR(255)"; ClearinghouseSource = "StudentSchoolEnrollment/GradeLevel/Description"; ClearinghouseObject = "S1"; Notes = "Grade name" }
)

Write-Host "Schema mapping loaded: $(($schemaMapping | Measure-Object).Count) table.column definitions" -ForegroundColor Green

# Export to CSV and JSON
$prefix = Join-Path $TracingFolder "psis-directory-schema-mapping"

# CSV export
$csvPath = "$prefix.csv"
$schemaMapping | Export-Csv -Path $csvPath -NoTypeInformation -Encoding UTF8
Write-Host "CSV: $csvPath" -ForegroundColor Green

# JSON export
$jsonPath = "$prefix.json"
$schemaMapping | ConvertTo-Json -Depth 5 | Out-File -FilePath $jsonPath -Encoding UTF8
Write-Host "JSON: $jsonPath" -ForegroundColor Green

# Create summary document
$summaryPath = Join-Path $TracingFolder "PSIS-DIRECTORY-SCHEMA.md"
$summary = @"
# PSIS and Directory Schema Mapping

Comprehensive mapping of PSIS and Directory production database tables back to Clearinghouse SIF sources.

## Table Summary

| Table | Purpose | Clearinghouse Source |
|-------|---------|----------------------|
| PSIS.PSIS_DISTRICT_MEMBERSHIP | Top-level student identity (district context) | StudentPersonal + manifest properties |
| PSIS.PSIS_PRI_FAC_MEMBERSHIP | Primary facility (school) enrollment record | StudentSchoolEnrollment + StudentAttendanceSummary |
| PSIS.GRADE_MEMBERSHIP | Grade-level enrollment with demographics flags | StudentPersonal demographics + StudentParticipation programs |
| PSIS.PSIS_SCRAM_MEMBERSHIP | Special education (SCRAM) program membership | StudentParticipation SPED records |
| PSIS.LU_* | Lookup tables (exit types, ELL, resident status, etc.) | Various SIF codes and descriptions |
| DIRECTORY.ORGANIZATION | LEA and School reference data | LEAInfo + SchoolInfo |
| DIRECTORY.Z0_GRADE | Grade level codes and descriptions | StudentSchoolEnrollment/GradeLevel |

## Column Mapping Format

Each entry contains:
- **Table**: Schema.TableName
- **Column**: Column name
- **DataType**: SQL data type
- **ClearinghouseSource**: Direct SIF XPath or description
- **ClearinghouseObject**: SIF manifest domain code (DI, SC, SL, S1, S2, etc.)
- **Notes**: Comments on derivation, constraints, or special handling

## Key Relationships

### Student Identity Hierarchy
1. PSIS.PSIS_DISTRICT_MEMBERSHIP (StudentPersonal identity in district context)
   ↓ FK: DISTRICT_MEMBERSHIP_ID
2. PSIS.PSIS_PRI_FAC_MEMBERSHIP (Enrollment at school)
   ↓ FK: PRI_FAC_MEMBERSHIP_ID
3. PSIS.GRADE_MEMBERSHIP (Grade-level details and demographics flags)
   ↓ FK: GRADE_MEMBERSHIP_ID
4. PSIS.PSIS_SCRAM_MEMBERSHIP (Special ed overlay, if applicable)

### Foreign Key References
- PSIS_DISTRICT_MEMBERSHIP.EXIT_TYPE_ID → PSIS.LU_EXIT_TYPE
- GRADE_MEMBERSHIP.FREE_RED_LUNCH_ID → PSIS.LU_FREE_RED_LUNCH
- GRADE_MEMBERSHIP.LIMITED_ENGLISH_ID → PSIS.LU_LIMITED_ENGLISH
- GRADE_MEMBERSHIP.RESIDENT_STATUS_ID → PSIS.LU_RESIDENT_STATUS
- GRADE_MEMBERSHIP.HOMELESS_ID → PSIS.LU_HOMELESS
- GRADE_MEMBERSHIP.GRADE_ID → DIRECTORY.Z0_GRADE
- PSIS_PRI_FAC_MEMBERSHIP.PRI_ORGANIZATION_ID → DIRECTORY.ORGANIZATION (School)
- PSIS_DISTRICT_MEMBERSHIP.REPORTING_ORGANIZATION_ID → DIRECTORY.ORGANIZATION (LEA)

## Clearinghouse Domain Codes

- **DI**: District Information (LEAInfo, manifest properties)
- **SC**: School Information (SchoolInfo, CalendarSummary, TermInfo)
- **SL**: Student List (StudentPersonal identity resolution)
- **S1**: Student Primary (StudentPersonal + StudentSchoolEnrollment + StudentAttendanceSummary)
- **S2**: Student SCRAM (Special Ed) (StudentParticipation SPED payloads)
- **S3**: Student YIC (Youth in Custody) (StudentParticipation YIC payloads)
- **AC**: Academic Course Master (SectionInfo)
- **AM**: Academic Membership (StudentCourseAssociation)
- **ST**: Student Transcript (StudentAcademicRecord header)
- **TC**: Transcript Courses (StudentAcademicRecord course history)
- **TG**: Transcript Grades (StudentAcademicRecord grades)
- **TA**: Transcript Assessments (StudentAcademicRecord test history)

## Usage for Lineage Enrichment

Use this mapping artifact to complete field lineage traces:
1. Report output field references table.column from intermediate report query
2. Look up table.column in this artifact
3. Return ClearinghouseSource (SIF XPath) and ClearinghouseObject (domain code)
4. Record as "Via Lookup/Production Table" or "Via STG/PSIS Column" depending on inheritance

## Notes

- Staging tables (Stg_*) are covered in the unified journey table
- This artifact covers PSIS production and Directory reference tables
- Lookup table descriptions (DESC columns) are derived from code values and PSIS metadata
- Some fields from StudentPersonal/SIF_ExtendedElements require custom POCO parsing (marked with "UTExtensions")
- Exit date handling: some vendors report the last day IN (should be first day OUT) - standardized in transformation

"@

$summary | Out-File -FilePath $summaryPath -Encoding UTF8
Write-Host "Markdown guide: $summaryPath" -ForegroundColor Green

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
   -WorkingTraceabilitySource $TracingFolder `
   -SourceInputs @($PSCommandPath) `
   -OutputPaths @($csvPath, $jsonPath, $summaryPath)

Write-Host "`nSchema mapping artifact creation complete!" -ForegroundColor Green
Write-Host "Total schema.column definitions: $(($schemaMapping | Measure-Object).Count)" -ForegroundColor Cyan
