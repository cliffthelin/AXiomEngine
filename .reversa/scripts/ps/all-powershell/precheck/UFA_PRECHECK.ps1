<#
.SYNOPSIS
Hard precheck gate for UFA Run-All pipeline.
Blocks execution if any file/folder failure would occur at runtime.

Run from inside the ufa_new_data directory.
#>

Write-Host "`n=== UFA HARD PRECHECK: RUN-ALL SAFETY GATE ===`n" -ForegroundColor Cyan

# -----------------------------
# 1. Load appsettings.json
# -----------------------------
$ConfigPath = "appsettings.json"

if (-not (Test-Path $ConfigPath)) {
    Write-Host "❌ FATAL: appsettings.json not found." -ForegroundColor Red
    exit 1
}

try {
    $Config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
} catch {
    Write-Host "❌ FATAL: appsettings.json is not valid JSON." -ForegroundColor Red
    exit 1
}

Write-Host "✅ appsettings.json loaded"

# -----------------------------
# 2. Resolve paths safely
# -----------------------------
function Resolve-PathSafe {
    param($Path)
    if (-not $Path) { return $null }
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return $Path
    }
    return (Join-Path (Get-Location) $Path)
}

$Failures = @()

# -----------------------------
# 3. Required directories (auto-create)
# -----------------------------
$RequiredDirs = @(
    $Config.ufa_files,
    $Config.created_files,
    $Config.final_output,
    $Config.ml_models
)

foreach ($Dir in $RequiredDirs) {
    $Resolved = Resolve-PathSafe $Dir
    if (-not (Test-Path $Resolved)) {
        Write-Host "⚠️ Creating missing directory: $Resolved" -ForegroundColor Yellow
        try {
            New-Item -ItemType Directory -Path $Resolved -Force | Out-Null
        } catch {
            $Failures += "Cannot create directory: $Resolved"
        }
    } else {
        Write-Host "✅ Directory exists: $Resolved"
    }
}

# -----------------------------
# 4. Required input files
# -----------------------------
$SourceFile = Resolve-PathSafe (Join-Path $Config.ufa_files $Config.ufa_file_name)
if (-not (Test-Path $SourceFile)) {
    $Failures += "Missing source UFA file: $SourceFile"
} else {
    Write-Host "✅ Source file found: $($Config.ufa_file_name)"
}

if ($Config.exclusion_file) {
    $ExclusionFile = Resolve-PathSafe $Config.exclusion_file
    if (-not (Test-Path $ExclusionFile)) {
        $Failures += "Missing exclusion file: $ExclusionFile"
    } else {
        Write-Host "✅ Exclusion file found"
    }
}

# -----------------------------
# 5. Required notebooks
# -----------------------------
$NotebookRoot = Resolve-PathSafe $Config.notebooks_dir
$AllNotebooks = @(
    $Config.prep_notebook
) + $Config.training_notebooks + $Config.reporting_notebooks

foreach ($NB in $AllNotebooks) {
    $NBPath = Join-Path $NotebookRoot $NB
    if (-not (Test-Path $NBPath)) {
        $Failures += "Missing notebook: $NB"
    } else {
        Write-Host "✅ Notebook found: $NB"
    }
}

# -----------------------------
# 6. Python environment
# -----------------------------
$PythonExe = Resolve-PathSafe $Config.python_path

if (-not $PythonExe -or -not (Test-Path $PythonExe)) {
    $Failures += "Python interpreter not found: $($Config.python_path)"
} else {
    Write-Host "✅ Python interpreter found"
}

# -----------------------------
# 7. Final decision
# -----------------------------
Write-Host "`n=== PRECHECK RESULT ===" -ForegroundColor Cyan

if ($Failures.Count -gt 0) {
    Write-Host "❌ PRECHECK FAILED — DO NOT RUN PIPELINE" -ForegroundColor Red
    Write-Host ""
    foreach ($F in $Failures) {
        Write-Host " - $F" -ForegroundColor Yellow
    }
    exit 1
}

Write-Host "✅ ALL CHECKS PASSED — SAFE TO RUN RUN-ALL NOTEBOOK" -ForegroundColor Green
Write-Host "`n=============================================`n"
exit 0
