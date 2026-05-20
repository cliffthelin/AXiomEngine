param(
    [string]$RootPath = 'C:\Projects\GITHUB',
    [string]$SeedCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-index-seed.csv',
    [string]$AliasCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-aliases.csv',
    [string]$OutputJsonPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-index.json',
    [string]$OutputFieldsCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-output-fields.csv',
    [string]$OutputFieldsByFieldCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-output-fields-by-field.csv',
    [string]$BuildFieldsCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-build-fields.csv',
    [string]$BuildFieldsByFieldCsvPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-build-fields-by-field.csv',
    [string]$OutputLineageJsonPath = 'C:\Projects\GITHUB\UTREx_SIF_VRF-develop\_reversa_sdd\traceability\master-reports-output-lineage.json'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$RepoNamePattern = '^(?<repo>[^\\/]+)[\\/]'

function Get-RepoNameFromRelativePath {
    param(
        [string]$RelativePath
    )

    if ($RelativePath -match $RepoNamePattern) {
        return $Matches['repo']
    }
    return ''
}

function Normalize-SqlObjectName {
    param(
        [string]$ObjectName
    )

    if ([string]::IsNullOrWhiteSpace($ObjectName)) {
        return ''
    }

    $normalized = $ObjectName.Trim()
    $normalized = $normalized -replace '\[', ''
    $normalized = $normalized -replace '\]', ''
    $normalized = $normalized -replace '\s+', ''
    return $normalized
}

function Normalize-FieldName {
    param(
        [string]$Value
    )

    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ''
    }

    $normalized = $Value.ToUpperInvariant()
    $normalized = $normalized -replace '[^A-Z0-9]+', ''
    return $normalized
}

function Get-PlainTextFriendlyNameFallback {
    param(
        [string]$FileName
    )

    $stem = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    $stem = $stem -replace '^rpt', ''
    $stem = $stem -replace '_', ' '
    $tokens = [regex]::Matches($stem, '[A-Z]+(?=$|[A-Z][a-z])|[A-Z]?[a-z]+|[0-9]+') | ForEach-Object { $_.Value }
    if ($tokens.Count -eq 0) {
        return ($stem -replace '\s+', ' ').Trim()
    }
    if ($tokens[-1] -eq 'Rpt') {
        $tokens[-1] = 'Report'
    }
    return (($tokens -join ' ') -replace '\s+', ' ').Trim()
}

function Get-PeriodTag {
    param(
        [string]$FileName,
        [string[]]$CommandTexts
    )

    $joined = @($FileName) + $CommandTexts -join ' '
    if ($joined -match 'December|Mid|MOY') { return 'MOY' }
    if ($joined -match 'Cumulative|End|EOY') { return 'EOY' }
    if ($joined -match 'October|Beg|BOY|Oct1') { return 'BOY' }
    if ($joined -match 'ActiveReg|Transfer|StudentSummary|GradeRange|Reading|WIDA|Graduation|DistrictOfResidence') { return 'YR' }
    return ''
}

function Get-ScopeTag {
    param(
        [string]$FileName,
        [string[]]$CommandTexts
    )

    $joined = @($FileName) + $CommandTexts -join ' '
    $hasSea = $joined -match '(^|[^A-Z])SEA([^A-Z]|$)|_SEA|State'
    $hasLea = $joined -match '(^|[^A-Z])LEA([^A-Z]|$)|District|Lea'
    if ($hasSea -and $hasLea) { return 'SEA_LEA' }
    if ($hasSea) { return 'SEA' }
    if ($hasLea) { return 'LEA' }
    return ''
}

function Get-TitleCandidates {
    param(
        [xml]$Xml,
        [System.Xml.XmlNamespaceManager]$Ns
    )

    $valueNodes = $Xml.SelectNodes('//def:Textbox/def:Paragraphs/def:Paragraph/def:TextRuns/def:TextRun/def:Value', $Ns)
    $candidates = New-Object System.Collections.Generic.List[string]
    foreach ($node in $valueNodes) {
        $value = [string]$node.InnerText
        if ([string]::IsNullOrWhiteSpace($value)) { continue }
        $trimmed = $value.Trim()
        if ($trimmed.StartsWith('=')) { continue }
        if ($trimmed.Length -lt 6) { continue }
        if ($trimmed -match 'Report|Summary|Membership|Registration|Students|Graduation|Reading|SCRAM|WIDA|Residence|Class List|Enrollment') {
            [void]$candidates.Add(($trimmed -replace '\s+', ' '))
        }
    }
    return $candidates.ToArray()
}

function Get-TitleCandidateScore {
    param(
        [string]$Title
    )

    $score = 0
    if ($Title -match '^Clearinghouse Report') { $score += 60 }
    if ($Title -match '\bReport\b') { $score += 40 }
    if ($Title -match '\bSummary\b|\bMembership\b|\bRegistration\b|\bStudents\b|\bGraduation\b|\bReading\b|\bSCRAM\b|\bWIDA\b|\bResidence\b|\bEnrollment\b') { $score += 20 }
    if ($Title -match 'Chart|Textbox|Label|Execution Time') { $score -= 30 }
    if ($Title.Length -gt 12) { $score += 5 }
    return $score
}

function Select-FriendlyName {
    param(
        [string[]]$TitleCandidates,
        [string]$FileName
    )

    $candidateArray = @($TitleCandidates | Where-Object { -not [string]::IsNullOrWhiteSpace($_) } | Sort-Object -Unique)
    if ($candidateArray.Count -eq 0) {
        return [pscustomobject]@{
            FriendlyName = Get-PlainTextFriendlyNameFallback -FileName $FileName
            AlternateTitles = @()
            UsedFallback = $true
        }
    }

    $scored = foreach ($candidate in $candidateArray) {
        [pscustomobject]@{
            title = $candidate
            score = Get-TitleCandidateScore -Title $candidate
        }
    }

    $selected = $scored | Sort-Object @{ Expression = 'score'; Descending = $true }, @{ Expression = 'title'; Descending = $false } | Select-Object -First 1
    return [pscustomobject]@{
        FriendlyName = $selected.title
        AlternateTitles = @($candidateArray | Where-Object { $_ -ne $selected.title })
        UsedFallback = $false
    }
}

function Get-InlineSqlArtifacts {
    param(
        [string[]]$CommandTexts
    )

    $tables = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    $buildFields = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)

    foreach ($commandText in $CommandTexts) {
        if ([string]::IsNullOrWhiteSpace($commandText)) { continue }
        if ($commandText -match '^\s*SELECT\b' -or $commandText -match '\bFROM\b') {
            foreach ($match in [regex]::Matches($commandText, '(?im)\b(?:FROM|JOIN|APPLY|INTO|UPDATE)\s+((?:\[[^\]]+\]|[A-Za-z0-9_]+)(?:\.(?:\[[^\]]+\]|[A-Za-z0-9_]+)){0,3})')) {
                [void]$tables.Add($match.Groups[1].Value.Trim())
            }
            foreach ($match in [regex]::Matches($commandText, '(?im)(?:^|,|\s)([A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*)')) {
                [void]$buildFields.Add($match.Groups[1].Value.Trim())
            }
        }
    }

    return [pscustomobject]@{
        TablesUsed = @($tables | Sort-Object)
        BuildFields = @($buildFields | Sort-Object)
    }
}

function Get-SqlObjects {
    param(
        [string[]]$CommandTexts,
        [string[]]$CommandTypes
    )

    $objects = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    for ($index = 0; $index -lt $CommandTexts.Count; $index++) {
        $commandText = $CommandTexts[$index]
        $commandType = if ($index -lt $CommandTypes.Count) { $CommandTypes[$index] } else { '' }
        if ([string]::IsNullOrWhiteSpace($commandText)) { continue }
        if ($commandType -eq 'StoredProcedure' -or $commandText -match '^[A-Za-z0-9_\[\]\.]+$') {
            [void]$objects.Add($commandText.Trim())
        }
    }
    return @($objects | Sort-Object)
}

function Get-ReferencedTablesFromText {
    param(
        [string]$Content
    )

    $tables = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    if ([string]::IsNullOrWhiteSpace($Content)) {
        return @()
    }

    foreach ($match in [regex]::Matches($Content, '(?im)\b(?:FROM|JOIN|APPLY|INTO|UPDATE|MERGE\s+INTO)\s+((?:\[[^\]]+\]|[A-Za-z0-9_]+)(?:\.(?:\[[^\]]+\]|[A-Za-z0-9_]+)){0,3})')) {
        [void]$tables.Add($match.Groups[1].Value.Trim())
    }

    return @($tables | Sort-Object)
}

function Get-ColumnReferencesFromExpression {
    param(
        [string]$Expression
    )

    $references = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    if ([string]::IsNullOrWhiteSpace($Expression)) {
        return @()
    }

    foreach ($match in [regex]::Matches($Expression, '(?i)\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*(\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_]*)\b')) {
        [void]$references.Add(($match.Groups[1].Value.Trim() + '.' + ($match.Groups[2].Value.Trim() -replace '^\[|\]$', '')))
    }

    $reservedWords = @(
        'SELECT','DISTINCT','CASE','WHEN','THEN','ELSE','END','NULL','ISNULL','LEN','REPLACE','RTRIM','LTRIM','TRIM',
        'CAST','CONVERT','TRY_CAST','TRY_CONVERT','ROW_NUMBER','OVER','PARTITION','BY','ORDER','ASC','DESC','AND','OR',
        'NOT','IN','ON','AS','FROM','JOIN','LEFT','RIGHT','INNER','OUTER','FULL','CROSS','APPLY','WHERE','GROUP','TOP',
        'SUM','MIN','MAX','COUNT','AVG','DATEADD','DATEDIFF','SUBSTRING','COALESCE','NULLIF','UPPER','LOWER','LIKE'
    )
    $reservedIndex = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($word in $reservedWords) {
        [void]$reservedIndex.Add($word)
    }

    $expressionWithoutQualifiedReferences = [regex]::Replace($Expression, '(?i)\b([A-Za-z_][A-Za-z0-9_]*)\s*\.\s*(\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_]*)\b', ' ')
    foreach ($match in [regex]::Matches($expressionWithoutQualifiedReferences, '(?i)\b(\[?[A-Za-z_][A-Za-z0-9_]*\]?)\b')) {
        $token = ($match.Groups[1].Value -replace '^\[|\]$', '')
        if ([string]::IsNullOrWhiteSpace($token)) { continue }
        if ($reservedIndex.Contains($token)) { continue }
        if ($token -match '^[0-9]+$') { continue }
        if ($Expression -match ('(?i)\b' + [regex]::Escape($token) + '\s*\(')) { continue }
        [void]$references.Add($token)
    }

    return @($references | Sort-Object)
}

function Split-SqlExpressionList {
    param(
        [string]$Expression
    )

    if ([string]::IsNullOrWhiteSpace($Expression)) {
        return @()
    }

    $segments = New-Object System.Collections.Generic.List[string]
    $current = New-Object System.Text.StringBuilder
    $parenthesisDepth = 0
    $bracketDepth = 0
    $inSingleQuote = $false
    $characters = $Expression.ToCharArray()

    for ($index = 0; $index -lt $characters.Length; $index++) {
        $character = $characters[$index]

        if ($character -eq "'") {
            [void]$current.Append($character)
            if ($inSingleQuote -and $index + 1 -lt $characters.Length -and $characters[$index + 1] -eq "'") {
                $index += 1
                [void]$current.Append($characters[$index])
                continue
            }
            $inSingleQuote = -not $inSingleQuote
            continue
        }

        if (-not $inSingleQuote) {
            if ($character -eq '(') { $parenthesisDepth += 1 }
            elseif ($character -eq ')' -and $parenthesisDepth -gt 0) { $parenthesisDepth -= 1 }
            elseif ($character -eq '[') { $bracketDepth += 1 }
            elseif ($character -eq ']' -and $bracketDepth -gt 0) { $bracketDepth -= 1 }
            elseif ($character -eq ',' -and $parenthesisDepth -eq 0 -and $bracketDepth -eq 0) {
                $segment = $current.ToString().Trim()
                if (-not [string]::IsNullOrWhiteSpace($segment)) {
                    [void]$segments.Add($segment)
                }
                [void]$current.Clear()
                continue
            }
        }

        [void]$current.Append($character)
    }

    $finalSegment = $current.ToString().Trim()
    if (-not [string]::IsNullOrWhiteSpace($finalSegment)) {
        [void]$segments.Add($finalSegment)
    }

    return @($segments)
}

function Get-SqlAliasMap {
    param(
        [string]$Content
    )

    $aliasMap = @{}
    if ([string]::IsNullOrWhiteSpace($Content)) {
        return $aliasMap
    }

    foreach ($match in [regex]::Matches($Content, '(?im)\b(?:FROM|JOIN)\s+((?:\[[^\]]+\]|[A-Za-z0-9_]+)(?:\.(?:\[[^\]]+\]|[A-Za-z0-9_]+)){0,3})\s+(?:AS\s+)?([A-Za-z_][A-Za-z0-9_]*)')) {
        $tableName = ($match.Groups[1].Value.Trim() -replace '\[|\]', '')
        $aliasName = $match.Groups[2].Value.Trim()
        $aliasMap[$aliasName] = $tableName
    }

    return $aliasMap
}

function Get-FieldDefinitionCandidates {
    param(
        [string]$Content,
        [string]$TargetField
    )

    $candidates = @()
    if ([string]::IsNullOrWhiteSpace($Content) -or [string]::IsNullOrWhiteSpace($TargetField)) {
        return $candidates
    }

    $targetPattern = [regex]::Escape($TargetField)
    $lines = $Content -split "`r?`n"
    foreach ($line in $lines) {
        $trimmed = $line.Trim()
        if ([string]::IsNullOrWhiteSpace($trimmed)) { continue }
        if ($trimmed -match '^(?i)(FROM|JOIN|WHERE|GROUP\s+BY|ORDER\s+BY|UNION|HAVING)\b') { continue }

        $segmentSource = $trimmed -replace '^(?i)SELECT\s+DISTINCT\s+', ''
        $segmentSource = $segmentSource -replace '^(?i)SELECT\s+', ''
        $segments = Split-SqlExpressionList -Expression $segmentSource
        if ($segments.Count -eq 0) {
            $segments = @($segmentSource)
        }

        foreach ($segment in $segments) {
            $candidateText = $segment.Trim().Trim(',')
            if ([string]::IsNullOrWhiteSpace($candidateText)) { continue }

            if ($candidateText -match '(?i)\bAS\s+\[?' + $targetPattern + '\]?\b') {
                $expression = ($candidateText -replace '(?i)\bAS\s+\[?' + $targetPattern + '\]?\b.*$', '').Trim().Trim(',')
                if (-not [string]::IsNullOrWhiteSpace($expression)) {
                    $candidates += [pscustomobject]@{ expression = $expression; source_line = $trimmed; match_type = 'as_alias' }
                }
                continue
            }

            if ($candidateText -match '(?i)^,?\s*(.+?)\s+\[?' + $targetPattern + '\]?\s*,?$') {
                $expression = $Matches[1].Trim().Trim(',')
                if (-not [string]::IsNullOrWhiteSpace($expression) -and $expression -ne $TargetField) {
                    $candidates += [pscustomobject]@{ expression = $expression; source_line = $trimmed; match_type = 'implicit_alias' }
                }
                continue
            }

            if ($candidateText -match '(?i)^,?\s*([A-Za-z_][A-Za-z0-9_]*)\.\[?' + $targetPattern + '\]?\s*,?$') {
                $expression = ($Matches[1] + '.' + $TargetField)
                $candidates += [pscustomobject]@{ expression = $expression; source_line = $trimmed; match_type = 'passthrough' }
            }
        }
    }

    return @($candidates | Select-Object -Unique expression,source_line,match_type)
}

function New-ClearinghouseHintIndex {
    $hintRows = @(
        [pscustomobject]@{ normalized='LEANUMBER'; object='District Record'; code='DI'; field='LEA NUMBER'; sif='LEAInfo/StateProvinceId'; source='PSIS.Stg_District.LeaNumber|Directory.ORGANIZATION.ORGANIZATION_ID|DISTRICT_NUMBER|DistCode' },
        [pscustomobject]@{ normalized='SCHOOLYEAR'; object='District Record'; code='DI'; field='SchoolYear'; sif='manifest property Vrf.Property.CurrentSchoolYear'; source='PSIS.Stg_District.SchoolYear|USOE.SchoolsByYear.SchoolYear|SCHOOL_YEAR' },
        [pscustomobject]@{ normalized='STUDENTNUMBER'; object='Student Record'; code='S1'; field='StudentNumber'; sif='StudentPersonal/LocalId'; source='PSIS.stg_student.StudentNumber|PSIS.PSIS_DISTRICT_MEMBERSHIP.DISTRICT_STUDENT_ID|DISTRICT_STUDENT_ID|Student_Id' },
        [pscustomobject]@{ normalized='STATEWIDESTUDENTID'; object='Student Record'; code='S1'; field='StatewideStudentID'; sif='StudentPersonal/StateProvinceId'; source='PSIS.stg_student.StatewideStudentID|PSIS.PSIS_DISTRICT_MEMBERSHIP.SASID|SASID' },
        [pscustomobject]@{ normalized='LASTNAME'; object='Student Record'; code='S1'; field='LastName'; sif='StudentPersonal/PersonInfo/Name/LastName'; source='PSIS.stg_student.LastName|PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_LAST_NAME|FORMAL_LAST_NAME' },
        [pscustomobject]@{ normalized='FIRSTNAME'; object='Student Record'; code='S1'; field='FirstName'; sif='StudentPersonal/PersonInfo/Name/FirstName'; source='PSIS.stg_student.FirstName|PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_FIRST_NAME|FORMAL_FIRST_NAME' },
        [pscustomobject]@{ normalized='MIDDLENAME'; object='Student Record'; code='S1'; field='MiddleName'; sif='StudentPersonal/PersonInfo/Name/MiddleName'; source='PSIS.stg_student.MiddleName|PSIS.PSIS_DISTRICT_MEMBERSHIP.FORMAL_MIDDLE_NAME|FORMAL_MIDDLE_NAME' },
        [pscustomobject]@{ normalized='BIRTHDATE'; object='Student Record'; code='S1'; field='BirthDate'; sif='StudentPersonal/PersonInfo/Demographics/BirthDate'; source='PSIS.stg_student.BirthDate|PSIS.PSIS_DISTRICT_MEMBERSHIP.DATE_OF_BIRTH|DATE_OF_BIRTH' },
        [pscustomobject]@{ normalized='GENDER'; object='Student Record'; code='S1'; field='Gender'; sif='StudentPersonal/PersonInfo/Demographics/Sex'; source='PSIS.stg_student.Gender|PSIS.PSIS_DISTRICT_MEMBERSHIP.GENDER|GENDER' },
        [pscustomobject]@{ normalized='SCHOOLNUMBER'; object='StudentSchoolEnrollment'; code='S1'; field='SchoolNumber'; sif='StudentSchoolEnrollment/SchoolInfoRefId resolved'; source='PSIS.stg_student.SchoolNumber|PSIS.PSIS_PRI_FAC_MEMBERSHIP.PRI_ORGANIZATION_ID|PRI_ORGANIZATION_ID|SCHOOL_NUMBER' },
        [pscustomobject]@{ normalized='ENTRYDATE'; object='StudentSchoolEnrollment'; code='S1'; field='EntryDate'; sif='StudentSchoolEnrollment/EntryDate'; source='PSIS.stg_student.EntryDate|PSIS.PSIS_PRI_FAC_MEMBERSHIP.ENTRY_DATE|ENTRY_DATE' },
        [pscustomobject]@{ normalized='EXITDATE'; object='StudentSchoolEnrollment'; code='S1'; field='ExitDate'; sif='StudentSchoolEnrollment/ExitDate'; source='PSIS.stg_student.ExitDate|PSIS.PSIS_PRI_FAC_MEMBERSHIP.EXIT_DATE|EXIT_DATE' },
        [pscustomobject]@{ normalized='GRADELEVEL'; object='StudentSchoolEnrollment'; code='S1'; field='GradeLevel'; sif='StudentSchoolEnrollment/GradeLevel/Code'; source='PSIS.stg_student.GradeLevel|PSIS.GRADE_MEMBERSHIP.GRADE_ID|GRADE_ID' }
    )

    $index = @{}
    foreach ($row in $hintRows) {
        foreach ($sourceToken in ($row.source -split '\|')) {
            $normalizedToken = Normalize-FieldName -Value $sourceToken
            if ([string]::IsNullOrWhiteSpace($normalizedToken)) { continue }
            if (-not $index.ContainsKey($normalizedToken)) {
                $index[$normalizedToken] = @()
            }
            $index[$normalizedToken] += [pscustomobject]@{
                clearinghouse_object_name = $row.object
                clearinghouse_code = $row.code
                field_name = $row.field
                sif_xpath = $row.sif
                matched_source = $sourceToken
            }
        }
    }

    return $index
}

function Get-ClearinghouseMatchesForReference {
    param(
        [string]$Reference,
        [hashtable]$HintIndex
    )

    $normalizedReference = Normalize-FieldName -Value $Reference
    if ([string]::IsNullOrWhiteSpace($normalizedReference)) {
        return @()
    }

    if ($HintIndex.ContainsKey($normalizedReference)) {
        return @($HintIndex[$normalizedReference] | Sort-Object field_name, matched_source -Unique)
    }

    return @()
}

function New-LineageNodeFromReference {
    param(
        [string]$Reference,
        [hashtable]$AliasMap,
        [hashtable]$HintIndex,
        [string]$SqlObjectName,
        [string]$Content,
        [hashtable]$Visited
    )

    if ([string]::IsNullOrWhiteSpace($Reference)) {
        return $null
    }

    $normalizedReference = Normalize-FieldName -Value $Reference
    if ($Visited.ContainsKey($normalizedReference)) {
        return [pscustomobject]@{ node_type = 'cycle_guard'; name = $Reference; children = @() }
    }
    $Visited[$normalizedReference] = $true

    $parts = $Reference -split '\.', 2
    if ($parts.Count -eq 2) {
        $aliasName = $parts[0]
        $columnName = ($parts[1] -replace '^\[|\]$', '')
        if ($AliasMap.ContainsKey($aliasName)) {
            $tableName = $AliasMap[$aliasName]
            $matches = @(Get-ClearinghouseMatchesForReference -Reference ($tableName + '.' + $columnName) -HintIndex $HintIndex)
            if ($matches.Count -eq 0) {
                $matches = @(Get-ClearinghouseMatchesForReference -Reference $columnName -HintIndex $HintIndex)
            }
            return [pscustomobject]@{
                node_type = 'table_column'
                name = $Reference
                table = $tableName
                column = $columnName
                clearinghouse_matches = @($matches)
                children = @()
            }
        }

        $candidateDefinitions = @(Get-FieldDefinitionCandidates -Content $Content -TargetField $columnName)
        if ($candidateDefinitions.Count -gt 0) {
            $children = @()
            foreach ($definition in $candidateDefinitions | Select-Object -First 3) {
            $expressionReferences = @(Get-ColumnReferencesFromExpression -Expression $definition.expression)
                if ($expressionReferences.Count -eq 0) {
                    $children += [pscustomobject]@{
                        node_type = 'expression'
                        name = $definition.expression
                        source_line = $definition.source_line
                        children = @()
                    }
                }
                else {
                    $grandChildren = @()
                    foreach ($expressionReference in $expressionReferences) {
                        $grandChild = New-LineageNodeFromReference -Reference $expressionReference -AliasMap $AliasMap -HintIndex $HintIndex -SqlObjectName $SqlObjectName -Content $Content -Visited $Visited
                        if ($null -ne $grandChild) {
                            $grandChildren += $grandChild
                        }
                    }
                    $children += [pscustomobject]@{
                        node_type = 'derived_alias'
                        name = $columnName
                        source_line = $definition.source_line
                        expression = $definition.expression
                        children = @($grandChildren)
                    }
                }
            }

            return [pscustomobject]@{
                node_type = 'derived_reference'
                name = $Reference
                sql_object = $SqlObjectName
                children = @($children)
            }
        }
    }

    $candidateDefinitions = @(Get-FieldDefinitionCandidates -Content $Content -TargetField ($Reference -replace '^\[|\]$', ''))
    if ($candidateDefinitions.Count -gt 0) {
        $children = @()
        foreach ($definition in $candidateDefinitions | Select-Object -First 3) {
            $expressionReferences = @(Get-ColumnReferencesFromExpression -Expression $definition.expression)
            if ($expressionReferences.Count -eq 0) {
                $children += [pscustomobject]@{
                    node_type = 'expression'
                    name = $definition.expression
                    source_line = $definition.source_line
                    children = @()
                }
            }
            else {
                $grandChildren = @()
                foreach ($expressionReference in $expressionReferences) {
                    $grandChild = New-LineageNodeFromReference -Reference $expressionReference -AliasMap $AliasMap -HintIndex $HintIndex -SqlObjectName $SqlObjectName -Content $Content -Visited $Visited
                    if ($null -ne $grandChild) {
                        $grandChildren += $grandChild
                    }
                }
                $children += [pscustomobject]@{
                    node_type = 'derived_alias'
                    name = $Reference
                    source_line = $definition.source_line
                    expression = $definition.expression
                    children = @($grandChildren)
                }
            }
        }

        return [pscustomobject]@{
            node_type = 'derived_reference'
            name = $Reference
            sql_object = $SqlObjectName
            children = @($children)
        }
    }

    $matches = @(Get-ClearinghouseMatchesForReference -Reference $Reference -HintIndex $HintIndex)
    return [pscustomobject]@{
        node_type = 'unresolved_reference'
        name = $Reference
        clearinghouse_matches = @($matches)
        children = @()
    }
}

function Get-OutputFieldLineageTree {
    param(
        [pscustomobject]$Dataset,
        [pscustomobject]$Field,
        [string]$ReportTag,
        [hashtable]$SearchIndex,
        [hashtable]$HintIndex,
        [string]$OwningRepo,
        [string]$RelativePath
    )

    $dataField = if ([string]::IsNullOrWhiteSpace($Field.data_field)) { $Field.field_name } else { $Field.data_field }
    $sqlObjectName = $Dataset.command_text
    $normalizedSqlObject = Normalize-SqlObjectName -ObjectName $sqlObjectName
    $sqlMatches = @()
    if (-not [string]::IsNullOrWhiteSpace($normalizedSqlObject) -and $SearchIndex.ContainsKey($normalizedSqlObject)) {
        $sqlMatches = @($SearchIndex[$normalizedSqlObject])
    }
    elseif (-not [string]::IsNullOrWhiteSpace($Dataset.command_text) -and $Dataset.command_text -match '^\s*SELECT\b') {
        $sqlMatches = @([pscustomobject]@{
            relative_path = $RelativePath
            repo_name = $OwningRepo
            tables_used = @(Get-ReferencedTablesFromText -Content $Dataset.command_text)
            content = $Dataset.command_text
        })
    }

    $sqlNodes = @()
    foreach ($sqlMatch in $sqlMatches | Select-Object -First 3) {
        $aliasMap = Get-SqlAliasMap -Content $sqlMatch.content
        $candidateDefinitions = @(Get-FieldDefinitionCandidates -Content $sqlMatch.content -TargetField $dataField)
        $definitionNodes = @()
        if ($candidateDefinitions.Count -eq 0) {
            $directReferenceNode = New-LineageNodeFromReference -Reference $dataField -AliasMap $aliasMap -HintIndex $HintIndex -SqlObjectName $sqlObjectName -Content $sqlMatch.content -Visited @{}
            if ($null -ne $directReferenceNode) {
                $definitionNodes += $directReferenceNode
            }
        }
        else {
            foreach ($definition in $candidateDefinitions | Select-Object -First 3) {
                $references = @(Get-ColumnReferencesFromExpression -Expression $definition.expression)
                $referenceNodes = @()
                foreach ($reference in $references) {
                    $referenceNode = New-LineageNodeFromReference -Reference $reference -AliasMap $aliasMap -HintIndex $HintIndex -SqlObjectName $sqlObjectName -Content $sqlMatch.content -Visited @{}
                    if ($null -ne $referenceNode) {
                        $referenceNodes += $referenceNode
                    }
                }
                if ($referenceNodes.Count -eq 0) {
                    $referenceNodes += [pscustomobject]@{
                        node_type = 'expression'
                        name = $definition.expression
                        source_line = $definition.source_line
                        children = @()
                    }
                }
                $definitionNodes += [pscustomobject]@{
                    node_type = 'sql_definition'
                    name = $dataField
                    expression = $definition.expression
                    source_line = $definition.source_line
                    children = @($referenceNodes)
                }
            }
        }

        $sqlNodes += [pscustomobject]@{
            node_type = 'sql_object'
            name = $sqlObjectName
            relative_path = $sqlMatch.relative_path
            repo_name = $sqlMatch.repo_name
            children = @($definitionNodes)
        }
    }

    return [pscustomobject]@{
        report_tag = $ReportTag
        dataset_name = $Dataset.dataset_name
        field_name = $Field.field_name
        data_field = $dataField
        lineage_tree = [pscustomobject]@{
            node_type = 'report_output_field'
            name = $Field.field_name
            children = @($sqlNodes)
        }
    }
}

function Resolve-SqlObjectEvidence {
    param(
        [string[]]$SqlObjects,
        [hashtable]$SearchIndex,
        [string]$RootPath,
        [string]$OwningRepo
    )

    $resolvedRepos = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    $resolvedTables = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    $evidence = @()
    [void]$resolvedRepos.Add($OwningRepo)

    foreach ($sqlObject in @($SqlObjects)) {
        if ([string]::IsNullOrWhiteSpace($sqlObject)) { continue }

        $normalizedSqlObject = Normalize-SqlObjectName -ObjectName $sqlObject

        $matches = @()
        if ($SearchIndex.ContainsKey($normalizedSqlObject)) {
            $matches = @($SearchIndex[$normalizedSqlObject])
        }

        if ($matches.Count -eq 0) {
            $evidence += [pscustomobject]@{
                sql_object = $sqlObject
                status = if ($sqlObject -like 'PSIS.*') { 'external_db_dependency' } else { 'unresolved' }
                matching_paths = @()
                candidate_tables = @()
            }
            continue
        }

        $candidateTables = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
        $matchingPaths = @()
        foreach ($match in $matches) {
            $matchingPaths += $match.relative_path
            [void]$resolvedRepos.Add($match.repo_name)
            foreach ($tableName in $match.tables_used) {
                [void]$candidateTables.Add($tableName)
                [void]$resolvedTables.Add($tableName)
            }
        }

        $evidence += [pscustomobject]@{
            sql_object = $sqlObject
            status = 'resolved_in_repo'
            matching_paths = @($matchingPaths | Sort-Object -Unique)
            candidate_tables = @($candidateTables | Sort-Object)
        }
    }

    return [pscustomobject]@{
        ReposUsed = @($resolvedRepos | Sort-Object)
        TablesUsed = @($resolvedTables | Sort-Object)
        Evidence = @($evidence)
    }
}

$searchableFiles = Get-ChildItem -Path $RootPath -Recurse -File -Include *.sql,*.ps1,*.config,*.xml,*.cs -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike '*\node_modules\*' -and $_.FullName -notlike '*\.git\*' }

$searchIndex = @{}
foreach ($searchableFile in $searchableFiles) {
    $relativePath = $searchableFile.FullName.Replace($RootPath + '\', '')
    $repoName = Get-RepoNameFromRelativePath -RelativePath $relativePath
    $fileContent = Get-Content -LiteralPath $searchableFile.FullName -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($fileContent)) { continue }

    foreach ($procMatch in [regex]::Matches($fileContent, '(?im)\b(?:CREATE|ALTER)\s+(?:PROC|PROCEDURE)\s+([A-Za-z0-9_\[\]\.]+)')) {
        $objectName = Normalize-SqlObjectName -ObjectName $procMatch.Groups[1].Value
        if (-not $searchIndex.ContainsKey($objectName)) {
            $searchIndex[$objectName] = @()
        }
        $searchIndex[$objectName] += [pscustomobject]@{
            relative_path = $relativePath
            repo_name = $repoName
            tables_used = @(Get-ReferencedTablesFromText -Content $fileContent)
            content = $fileContent
        }
    }
}

$clearinghouseHintIndex = New-ClearinghouseHintIndex

$aliasRows = @()
if (Test-Path -LiteralPath $AliasCsvPath) {
    $aliasRows = @(Import-Csv -Path $AliasCsvPath)
}

$aliasLookup = @{}
foreach ($aliasRow in $aliasRows) {
    $aliasList = @()
    if (-not [string]::IsNullOrWhiteSpace($aliasRow.aliases)) {
        $aliasList = @($aliasRow.aliases -split '\s*\|\s*' | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    }
    $aliasLookup[$aliasRow.report_tag] = [pscustomobject]@{
        preferred_friendly_name = $aliasRow.preferred_friendly_name
        aliases = $aliasList
    }
}

$seedRows = Import-Csv -Path $SeedCsvPath
$indexRows = @()

foreach ($row in $seedRows) {
    $absolutePath = Join-Path $RootPath $row.relative_path
    if (-not (Test-Path -LiteralPath $absolutePath)) {
        $indexRows += [pscustomobject]@{
            report_tag = $row.report_tag
            friendly_name = ''
            file_name = $row.file_name
            relative_path = $row.relative_path
            repo_name = $row.repo_name
            repo_code = $row.repo_code
            artifact_type_code = $row.artifact_type_code
            repos_used_for_it = @($row.repo_name)
            tables_used = @()
            output_fields = @()
            build_fields = @()
            sql_objects = @()
            data_sources = @()
            datasets = @()
            period_tag = ''
            scope_tag = ''
            match_status = 'missing_file'
            evidence_notes = @('Seed entry points to a file that does not exist at extraction time.')
        }
        continue
    }

    [xml]$xml = Get-Content -LiteralPath $absolutePath -Raw
    $ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
    $defaultNs = $xml.DocumentElement.NamespaceURI
    $ns.AddNamespace('def', $defaultNs)
    $ns.AddNamespace('rd', 'http://schemas.microsoft.com/SQLServer/reporting/reportdesigner')

    $datasetNodes = $xml.SelectNodes('//def:DataSets/def:DataSet', $ns)
    $datasetInfos = @()
    $allCommandTexts = New-Object System.Collections.Generic.List[string]
    $allCommandTypes = New-Object System.Collections.Generic.List[string]
    $allOutputFields = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    $allDataSources = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)

    foreach ($datasetNode in $datasetNodes) {
        $datasetName = $datasetNode.Attributes['Name'].Value
        $dataSourceName = $datasetNode.SelectSingleNode('def:Query/def:DataSourceName', $ns)
        $commandTypeNode = $datasetNode.SelectSingleNode('def:Query/def:CommandType', $ns)
        $commandTextNode = $datasetNode.SelectSingleNode('def:Query/def:CommandText', $ns)
        $fieldNodes = $datasetNode.SelectNodes('def:Fields/def:Field', $ns)
        $queryParameterNodes = $datasetNode.SelectNodes('def:Query/def:QueryParameters/def:QueryParameter', $ns)

        $fieldList = @()
        foreach ($fieldNode in $fieldNodes) {
            $fieldName = $fieldNode.Attributes['Name'].Value
            $dataFieldNode = $fieldNode.SelectSingleNode('def:DataField', $ns)
            $dataField = if ($null -ne $dataFieldNode) { [string]$dataFieldNode.InnerText } else { '' }
            [void]$allOutputFields.Add($fieldName)
            if (-not [string]::IsNullOrWhiteSpace($dataField)) {
                [void]$allOutputFields.Add($dataField)
            }
            $fieldList += [pscustomobject]@{
                field_name = $fieldName
                data_field = $dataField
            }
        }

        $parameterList = @()
        foreach ($parameterNode in $queryParameterNodes) {
            $parameterName = $parameterNode.Attributes['Name'].Value
            $parameterValueNode = $parameterNode.SelectSingleNode('def:Value', $ns)
            $parameterValue = if ($null -ne $parameterValueNode) { [string]$parameterValueNode.InnerText } else { '' }
            $parameterList += [pscustomobject]@{
                parameter_name = $parameterName
                value_expression = $parameterValue
            }
        }

        $commandType = if ($null -ne $commandTypeNode) { [string]$commandTypeNode.InnerText } else { '' }
        $commandText = if ($null -ne $commandTextNode) { [string]$commandTextNode.InnerText } else { '' }
        $dataSource = if ($null -ne $dataSourceName) { [string]$dataSourceName.InnerText } else { '' }

        if (-not [string]::IsNullOrWhiteSpace($commandText)) { [void]$allCommandTexts.Add($commandText) }
        if (-not [string]::IsNullOrWhiteSpace($commandType)) { [void]$allCommandTypes.Add($commandType) }
        if (-not [string]::IsNullOrWhiteSpace($dataSource)) { [void]$allDataSources.Add($dataSource) }

        $datasetInfos += [pscustomobject]@{
            dataset_name = $datasetName
            data_source_name = $dataSource
            command_type = $commandType
            command_text = $commandText
            query_parameters = @($parameterList)
            fields = @($fieldList)
        }
    }

    $titleCandidates = @(Get-TitleCandidates -Xml $xml -Ns $ns)
    $sqlObjects = @(Get-SqlObjects -CommandTexts $allCommandTexts.ToArray() -CommandTypes $allCommandTypes.ToArray())
    $inlineSqlArtifacts = Get-InlineSqlArtifacts -CommandTexts $allCommandTexts.ToArray()
    $friendlyNameSelection = Select-FriendlyName -TitleCandidates $titleCandidates -FileName $row.file_name
    $sqlResolution = Resolve-SqlObjectEvidence -SqlObjects $sqlObjects -SearchIndex $searchIndex -RootPath $RootPath -OwningRepo $row.repo_name
    $aliasRecord = if ($aliasLookup.ContainsKey($row.report_tag)) { $aliasLookup[$row.report_tag] } else { $null }
    $mergedTables = New-Object System.Collections.Generic.HashSet[string]([System.StringComparer]::OrdinalIgnoreCase)
    foreach ($tableName in @($inlineSqlArtifacts.TablesUsed) + @($sqlResolution.TablesUsed)) {
        if (-not [string]::IsNullOrWhiteSpace($tableName)) {
            [void]$mergedTables.Add($tableName)
        }
    }

    $notes = New-Object System.Collections.Generic.List[string]
    $friendlyName = $friendlyNameSelection.FriendlyName
    $friendlyNameSource = if ($friendlyNameSelection.UsedFallback) { 'fallback_file_name' } else { 'rdl_title' }
    $curatedAliases = @()
    if ($null -ne $aliasRecord) {
        $curatedAliases = @($aliasRecord.aliases | Sort-Object -Unique)
        if (-not [string]::IsNullOrWhiteSpace($aliasRecord.preferred_friendly_name)) {
            $friendlyName = $aliasRecord.preferred_friendly_name
            $friendlyNameSource = 'curated_alias'
        }
    }

    if ($friendlyNameSelection.UsedFallback) {
        [void]$notes.Add('Friendly name fell back to transformed file name because no rendered title candidate was found.')
    }
    elseif ($friendlyNameSelection.AlternateTitles.Count -gt 0) {
        [void]$notes.Add(('Alternate title candidates: ' + ($friendlyNameSelection.AlternateTitles -join ' | ')))
    }
    if ($sqlObjects.Count -gt 0) {
        [void]$notes.Add(('SQL objects referenced: ' + ($sqlObjects -join ' | ')))
    }
    $externalDependencies = @($sqlResolution.Evidence | Where-Object { $_.status -eq 'external_db_dependency' } | Select-Object -ExpandProperty sql_object)
    if ($externalDependencies.Count -gt 0) {
        [void]$notes.Add(('External database dependencies not defined in current repos: ' + ($externalDependencies -join ' | ')))
    }
    if ($curatedAliases.Count -gt 0) {
        [void]$notes.Add(('Curated aliases: ' + ($curatedAliases -join ' | ')))
    }
    if ($mergedTables.Count -eq 0 -and $sqlObjects.Count -gt 0) {
        [void]$notes.Add('Tables used are not yet resolved for stored procedure-backed datasets in the available repos.')
    }

    $outputFieldLineage = @()
    foreach ($datasetInfo in $datasetInfos) {
        foreach ($fieldInfo in $datasetInfo.fields) {
            $outputFieldLineage += @(Get-OutputFieldLineageTree -Dataset $datasetInfo -Field $fieldInfo -ReportTag $row.report_tag -SearchIndex $searchIndex -HintIndex $clearinghouseHintIndex -OwningRepo $row.repo_name -RelativePath $row.relative_path)
        }
    }

    $indexRows += [pscustomobject]@{
        report_tag = $row.report_tag
        friendly_name = $friendlyName
        friendly_name_source = $friendlyNameSource
        file_name = $row.file_name
        relative_path = $row.relative_path
        repo_name = $row.repo_name
        repo_code = $row.repo_code
        artifact_type_code = $row.artifact_type_code
        repos_used_for_it = @($sqlResolution.ReposUsed)
        tables_used = @($mergedTables | Sort-Object)
        output_fields = @($allOutputFields | Sort-Object)
        build_fields = @($inlineSqlArtifacts.BuildFields)
        curated_aliases = @($curatedAliases)
        sql_objects = @($sqlObjects)
        sql_object_evidence = @($sqlResolution.Evidence)
        data_sources = @($allDataSources | Sort-Object)
        datasets = @($datasetInfos)
        output_field_lineage = @($outputFieldLineage)
        period_tag = Get-PeriodTag -FileName $row.file_name -CommandTexts $allCommandTexts.ToArray()
        scope_tag = Get-ScopeTag -FileName $row.file_name -CommandTexts $allCommandTexts.ToArray()
        match_status = if ($externalDependencies.Count -gt 0) { 'metadata_extracted_external_sql_pending' } else { 'metadata_extracted' }
        evidence_notes = @($notes)
    }
}

$json = $indexRows | ConvertTo-Json -Depth 40
Set-Content -LiteralPath $OutputJsonPath -Value $json -Encoding UTF8

$outputFieldRows = foreach ($indexRow in $indexRows) {
    [pscustomobject]@{
        report_tag = $indexRow.report_tag
        friendly_name = $indexRow.friendly_name
        repo_name = $indexRow.repo_name
        file_name = $indexRow.file_name
        relative_path = $indexRow.relative_path
        output_field_count = @($indexRow.output_fields).Count
        output_fields = (@($indexRow.output_fields) -join ' | ')
    }
}
$outputFieldRows | Export-Csv -LiteralPath $OutputFieldsCsvPath -NoTypeInformation -Encoding UTF8

$outputFieldByFieldRows = foreach ($indexRow in $indexRows) {
    foreach ($outputField in @($indexRow.output_fields)) {
        [pscustomobject]@{
            report_tag = $indexRow.report_tag
            friendly_name = $indexRow.friendly_name
            repo_name = $indexRow.repo_name
            file_name = $indexRow.file_name
            relative_path = $indexRow.relative_path
            output_field = $outputField
        }
    }
}
$outputFieldByFieldRows | Export-Csv -LiteralPath $OutputFieldsByFieldCsvPath -NoTypeInformation -Encoding UTF8

$buildFieldRows = foreach ($indexRow in $indexRows) {
    [pscustomobject]@{
        report_tag = $indexRow.report_tag
        friendly_name = $indexRow.friendly_name
        repo_name = $indexRow.repo_name
        file_name = $indexRow.file_name
        relative_path = $indexRow.relative_path
        build_field_count = @($indexRow.build_fields).Count
        build_fields = (@($indexRow.build_fields) -join ' | ')
    }
}
$buildFieldRows | Export-Csv -LiteralPath $BuildFieldsCsvPath -NoTypeInformation -Encoding UTF8

$buildFieldByFieldRows = foreach ($indexRow in $indexRows) {
    foreach ($buildField in @($indexRow.build_fields)) {
        [pscustomobject]@{
            report_tag = $indexRow.report_tag
            friendly_name = $indexRow.friendly_name
            repo_name = $indexRow.repo_name
            file_name = $indexRow.file_name
            relative_path = $indexRow.relative_path
            build_field = $buildField
        }
    }
}
$buildFieldByFieldRows | Export-Csv -LiteralPath $BuildFieldsByFieldCsvPath -NoTypeInformation -Encoding UTF8

$lineageRows = foreach ($indexRow in $indexRows) {
    [pscustomobject]@{
        report_tag = $indexRow.report_tag
        friendly_name = $indexRow.friendly_name
        repo_name = $indexRow.repo_name
        file_name = $indexRow.file_name
        relative_path = $indexRow.relative_path
        output_field_lineage = @($indexRow.output_field_lineage)
    }
}
$lineageJson = $lineageRows | ConvertTo-Json -Depth 40
Set-Content -LiteralPath $OutputLineageJsonPath -Value $lineageJson -Encoding UTF8

& (Join-Path $PSScriptRoot 'Invoke-TraceabilityOutputStamp.ps1') `
    -WorkingTraceabilitySource (Split-Path -Parent $OutputJsonPath) `
    -SourceInputs @($PSCommandPath, $SeedCsvPath, $AliasCsvPath, $RootPath) `
    -OutputPaths @(
        $OutputJsonPath,
        $OutputFieldsCsvPath,
        $OutputFieldsByFieldCsvPath,
        $BuildFieldsCsvPath,
        $BuildFieldsByFieldCsvPath,
        $OutputLineageJsonPath
    )

Write-Output ("Wrote {0} report records to {1}" -f $indexRows.Count, $OutputJsonPath)
Write-Output ("Wrote output field summary to {0}" -f $OutputFieldsCsvPath)
Write-Output ("Wrote output field detail to {0}" -f $OutputFieldsByFieldCsvPath)
Write-Output ("Wrote build field summary to {0}" -f $BuildFieldsCsvPath)
Write-Output ("Wrote build field detail to {0}" -f $BuildFieldsByFieldCsvPath)
Write-Output ("Wrote output lineage tree export to {0}" -f $OutputLineageJsonPath)