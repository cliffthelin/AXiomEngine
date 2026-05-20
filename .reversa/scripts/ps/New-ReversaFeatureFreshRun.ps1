[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string[]]$ProjectPath,
    [switch]$AllInstalled,
    [string]$BaseSearchPath = 'C:\Projects\GITHUB',
    [string]$SandboxSuffix = 'reversa-fresh-run',
    [string]$OutputFolder = '_reversa_sdd_fresh',
    [ValidateSet('', 'feature', 'module', 'use-case', 'endpoint', 'hybrid', 'custom')]
    [string]$RecommendedOrganization = '',
    [string]$ReadmeFileName = 'FRESH-RUN-README.md'
)

$ErrorActionPreference = 'Stop'

function ConvertTo-TomlArray {
    param([object[]]$Values)

    if (-not $Values -or $Values.Count -eq 0) {
        return "[]"
    }

    $quoted = $Values | ForEach-Object { '  "{0}"' -f ($_ -replace '"', '\"') }
    return "[`n{0}`n]" -f ($quoted -join ",`n")
}

function New-UniqueSandboxPath {
    param(
        [string]$ProjectRoot,
        [string]$Suffix
    )

    $parent = Split-Path -Parent $ProjectRoot
    $name = Split-Path -Leaf $ProjectRoot
    $counter = 1
    $candidate = Join-Path $parent ("{0}-{1}-{2}" -f $name, $Suffix, $counter)

    while (Test-Path $candidate) {
        $counter += 1
        $candidate = Join-Path $parent ("{0}-{1}-{2}" -f $name, $Suffix, $counter)
    }

    return $candidate
}

function Get-ReversaProjectRoots {
    param([string]$SearchRoot)

    $results = New-Object System.Collections.Generic.List[string]
    $stateFiles = Get-ChildItem -Path $SearchRoot -Filter state.json -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Directory.Name -eq '.reversa' -and
            $_.FullName -notmatch '\\.reversa\\backups\\' -and
            $_.FullName -notmatch '-feature-fresh-run'
        }

    foreach ($stateFile in $stateFiles) {
        $root = Split-Path -Parent (Split-Path -Parent $stateFile.FullName)
        if (Test-Path (Join-Path $root 'FRESH-RUN-README.md')) {
            continue
        }
        if (-not $results.Contains($root)) {
            $results.Add($root)
        }
    }

    return $results.ToArray() | Sort-Object
}

function New-FreshSandbox {
    param(
        [string]$RepoRoot,
        [string]$Suffix,
        [string]$FreshOutputFolder,
        [string]$OrganizationRecommendation,
        [string]$ReadmeName
    )

    $statePath = Join-Path $RepoRoot '.reversa\state.json'
    $versionPath = Join-Path $RepoRoot '.reversa\version'

    if (-not (Test-Path $statePath)) {
        throw "No Reversa state found at $statePath"
    }

    $state = Get-Content -Raw $statePath | ConvertFrom-Json
    $version = if (Test-Path $versionPath) {
        (Get-Content -Raw $versionPath).Trim()
    } elseif ($state.version) {
        [string]$state.version
    } else {
        '1.2.43'
    }

    $sandboxRoot = New-UniqueSandboxPath -ProjectRoot $RepoRoot -Suffix $Suffix
    $projectName = if ($state.project) { [string]$state.project } else { Split-Path -Leaf $RepoRoot }
    $userName = if ($state.user_name) { [string]$state.user_name } else { 'User' }
    $chatLanguage = if ($state.chat_language) { [string]$state.chat_language } else { 'English' }
    $docLanguage = if ($state.doc_language) { [string]$state.doc_language } else { 'English' }
    $answerMode = if ($state.answer_mode) { [string]$state.answer_mode } else { 'chat' }
    $forwardFolder = if ($state.forward_folder) { [string]$state.forward_folder } else { '_reversa_forward' }
    $engines = @($state.engines)
    $agents = @($state.agents)
    $recommendedOrganizationText = if ($OrganizationRecommendation) {
        "`nOptional recommendation:`n4. When Reversa asks for organization, choose ``$OrganizationRecommendation``.`n"
    } else {
        ''
    }
    $expectedRecommendationText = if ($OrganizationRecommendation) {
        "- This run is set up generically, with a recommendation to choose ``$OrganizationRecommendation`` when prompted.`n"
    } else {
        "- This run is set up generically. Reversa will ask you how to organize specs during the run.`n"
    }

    if ($PSCmdlet.ShouldProcess($sandboxRoot, "Create fresh Reversa sandbox for $RepoRoot")) {
        New-Item -ItemType Directory -Path $sandboxRoot -Force | Out-Null

        Get-ChildItem -LiteralPath $RepoRoot -Force | ForEach-Object {
            if ($_.Name -eq '.reversa' -or $_.Name -eq '.git' -or $_.Name -like '_reversa*') {
                return
            }

            $destination = Join-Path $sandboxRoot $_.Name

            if ($_.PSIsContainer) {
                New-Item -ItemType Junction -Path $destination -Target $_.FullName | Out-Null
            } else {
                Copy-Item -LiteralPath $_.FullName -Destination $destination -Force
            }
        }

        $reversaDir = Join-Path $sandboxRoot '.reversa'
        New-Item -ItemType Directory -Path $reversaDir -Force | Out-Null

        $configToml = @"
# Reversa — Project Configuration
# This sandbox is isolated from the original extraction.

[project]
name = "$projectName"
version = "1.0.0"

[user]
name = "$userName"
chat_language = "$chatLanguage"
doc_language = "$docLanguage"

[output]
folder = "$FreshOutputFolder"

[agents]
installed = $(ConvertTo-TomlArray -Values $agents)

[engines]
installed = $(ConvertTo-TomlArray -Values $engines)

[analysis]
answer_mode = "$answerMode"
doc_level = ""
"@

        $freshState = [ordered]@{
            version = $version
            project = $projectName
            user_name = $userName
            chat_language = $chatLanguage
            doc_language = $docLanguage
            answer_mode = $answerMode
            doc_level = $null
            output_folder = $FreshOutputFolder
            forward_folder = $forwardFolder
            phase = $null
            completed = @()
            pending = @('reconhecimento', 'escavacao', 'interpretacao', 'geracao', 'revisao')
            checkpoints = [ordered]@{}
            engines = $engines
            agents = $agents
            created_files = @(
                '.reversa/version',
                '.reversa/config.toml',
                '.reversa/config.user.toml',
                '.reversa/state.json'
            )
        }

        $readme = @"
# Fresh Reversa Sandbox

This folder is an isolated sandbox for a new Reversa extraction.

What is isolated:
- `.reversa/state.json` is reset to a first-run state.
- Output will go to `$FreshOutputFolder/`.
- No existing `_reversa_sdd/` artifacts from the original project are reused.

What is shared:
- The legacy source tree is referenced through junctions.
- The installed Reversa skills are referenced through junctions.

How to use:
1. Open this folder in VS Code as its own workspace folder.
2. Type `/reversa`.
3. Approve the newly generated plan.
$recommendedOrganizationText

Expected behavior:
- This run will analyze the same codebase.
- It will not resume the old extraction.
- It will write new artifacts under `$FreshOutputFolder/`.
$expectedRecommendationText
"@

        Set-Content -LiteralPath (Join-Path $reversaDir 'version') -Value $version -Encoding UTF8
        Set-Content -LiteralPath (Join-Path $reversaDir 'config.user.toml') -Value "# Reversa — Personal Settings`n# This file is for your personal overrides.`n" -Encoding UTF8
        Set-Content -LiteralPath (Join-Path $reversaDir 'config.toml') -Value $configToml -Encoding UTF8
        Set-Content -LiteralPath (Join-Path $reversaDir 'state.json') -Value ($freshState | ConvertTo-Json -Depth 20) -Encoding UTF8
        Set-Content -LiteralPath (Join-Path $sandboxRoot $ReadmeName) -Value $readme -Encoding UTF8
    }

    [pscustomobject]@{
        ProjectRoot = $RepoRoot
        SandboxRoot = $sandboxRoot
        OutputFolder = $FreshOutputFolder
        Version = $version
    }
}

$targets = @()
if ($AllInstalled) {
    $targets = Get-ReversaProjectRoots -SearchRoot $BaseSearchPath
} elseif ($ProjectPath) {
    $targets = $ProjectPath | ForEach-Object { (Resolve-Path $_).Path }
}

if (-not $targets -or $targets.Count -eq 0) {
    throw 'Provide -ProjectPath <repoRoot> or use -AllInstalled.'
}

$results = foreach ($target in $targets) {
    New-FreshSandbox -RepoRoot $target -Suffix $SandboxSuffix -FreshOutputFolder $OutputFolder -OrganizationRecommendation $RecommendedOrganization -ReadmeName $ReadmeFileName
}

$results | Format-Table ProjectRoot, SandboxRoot, OutputFolder, Version -AutoSize