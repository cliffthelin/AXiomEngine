<#
.SYNOPSIS
    Advanced UFA Pipeline Pre-Check + Data Pivot Summary.
    Run this from inside the 'ufa_new_data' folder.
    Fully dynamic: All paths and filenames are sourced from appsettings.json.
    Validates if new data is present compared to the last completed run.
#>

# --- 1. CONFIGURATION & INITIALIZATION ---
$ConfigFile = "appsettings.json"
$ReportData = @()
$Failures   = @() # Track specific action items for the final summary

# Load Settings from Source of Truth
if (Test-Path $ConfigFile) {
    $JsonContent = Get-Content $ConfigFile -Raw
    $JsonData = $JsonContent | ConvertFrom-Json
} else {
    Write-Host "❌ Critical: $ConfigFile not found." -ForegroundColor Red
    exit 1
}

# Ensure dynamic tracking variables exist in the JSON object
if (-not $JsonData.output_pivot_basename) { $JsonData | Add-Member -Name "output_pivot_basename" -Value "UFA_Pivot_Summary" -MemberType NoteProperty }
if (-not $JsonData.Last_pivot_summary) { $JsonData | Add-Member -Name "Last_pivot_summary" -Value "" -MemberType NoteProperty }

# Map Dynamic Variables from JSON
$UfaFilesDir      = $JsonData.ufa_files
$ProductionModels = $JsonData.ml_models
$FinalOutputDir   = $JsonData.final_output
$NotebooksDir     = "." 
$ExclusionPath    = $JsonData.exclusion_file
$TrainingFilePath = "$($JsonData.training_file).csv"
$PivotBaseName    = $JsonData.output_pivot_basename

# --- 2. DYNAMIC FILE UPDATER & STALE DATA VALIDATION ---
Write-Host "--- DYNAMIC DATA VALIDATION ---" -ForegroundColor Yellow

# A. Detect Newest Source Data
$SourcePattern = "utah_fits_all___household_applications_criteria_and_enrollments_*.xlsx"
$SearchPath = Join-Path $UfaFilesDir $SourcePattern
$LatestSource = Get-ChildItem $SearchPath -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1

$NewDataDetected = $false
if ($LatestSource) {
    # Compare found file against JSON record
    if ($LatestSource.Name -ne $JsonData.ufa_file_name) {
        Write-Host "🔔 Newer source file detected: $($LatestSource.Name)" -ForegroundColor Cyan
        $JsonData.ufa_file_name = $LatestSource.Name
        $NewDataDetected = $true
        
        # Extract date (YYYY-MM-DD) and reformat to MM-DD-YYYY
        if ($LatestSource.Name -match "(\d{4}-\d{2}-\d{2})") {
            $JsonData.file_date = [datetime]::ParseExact($Matches[1], "yyyy-MM-dd", $null).ToString("MM-dd-yyyy")
        }
    } else {
        Write-Host "ℹ️ Source data matches current configuration." -ForegroundColor Gray
    }
} else {
    $Failures += "Missing Source Data: No .xlsx files found in '$UfaFilesDir' matching the Odyssey naming convention."
}

# B. Detect Last Completed Pivot Summary & Check for Stale State
$PivotPattern = "$PivotBaseName*.xlsx"
$LatestPivot = Get-ChildItem (Join-Path $FinalOutputDir $PivotPattern) -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1

if ($LatestPivot) {
    $JsonData.Last_pivot_summary = $LatestPivot.Name
    
    # FAILURE LOGIC: Source must be newer than the last completed pivot
    if ($LatestSource) {
        if (-not $NewDataDetected -and ($LatestSource.LastWriteTime -le $LatestPivot.LastWriteTime)) {
            $Failures += "Stale Data: The latest source file is not newer than the last pivot summary. Action: Please place a new export in '$UfaFilesDir'."
        }
    }
}

# Save all dynamic updates back to appsettings.json
$JsonData | ConvertTo-Json -Depth 4 | Set-Content $ConfigFile
Write-Host "💾 appsettings.json synchronized with latest directory state." -ForegroundColor Gray

# --- 3. SMART ENVIRONMENT CHECK ---
Write-Host "`n--- SYSTEM DEPENDENCY CHECK ---" -ForegroundColor Yellow

$CachedPython = $JsonData.python_path
$ActivePython = $null

# A. CHECK CACHE
if ($CachedPython -and (Test-Path $CachedPython)) {
    try {
        $ver = & $CachedPython --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Cache Hit: Using Python ($ver)" -ForegroundColor Green
            $ActivePython = $CachedPython
        }
    } catch {
        Write-Host "⚠️ Cached path invalid. Initiating search..." -ForegroundColor Yellow
    }
}

# B. AUTO-DISCOVERY
if (-not $ActivePython) {
    Write-Host "🔍 Searching for virtual environments..." -ForegroundColor Cyan
    $VenvCandidates = @(
        Get-ChildItem -Path "." -Directory -Filter "*venv*",
        Get-ChildItem -Path ".." -Directory -Filter "*venv*"
    )
    if ($VenvCandidates) { 
        $VenvCandidates = $VenvCandidates | Select-Object -ExpandProperty FullName -Unique 
    }

    foreach ($VenvPath in $VenvCandidates) {
        $WinPath = Join-Path $VenvPath "Scripts\python.exe"
        if (Test-Path $WinPath) {
            $ActivePython = $WinPath
            Write-Host "✅ Found existing venv: $VenvPath" -ForegroundColor Green
            break
        }
    }
}

# C. PROMPT OR CREATE
if (-not $ActivePython) {
    Write-Host "❌ No environment found. Manual entry or auto-create in 30s..." -ForegroundColor Yellow
    
    $ManualPath = $null
    $Timeout = 30
    $Timer = [System.Diagnostics.Stopwatch]::StartNew()
    
    while ($Timer.Elapsed.TotalSeconds -lt $Timeout) {
        if ([Console]::KeyAvailable) {
            $ManualPath = Read-Host "   Enter full path to python.exe (or press Enter to skip)"
            break
        }
        Start-Sleep -Milliseconds 100
    }
    
    if ($ManualPath -and (Test-Path $ManualPath)) {
        $ActivePython = $ManualPath
    } else {
        Write-Host "`n⚡ Timeout/Skip detected. Creating new environment 'ufa_venv'..." -ForegroundColor Cyan
        try { python --version | Out-Null } catch { 
            Write-Host "❌ FATAL: Base 'python' not found in PATH." -ForegroundColor Red; exit 1 
        }
        $NewVenvPath = "..\ufa_venv"
        python -m venv $NewVenvPath
        $ActivePython = Join-Path $NewVenvPath "Scripts\python.exe"
        
        if (Test-Path $ActivePython) {
            Write-Host "📦 Installing requirements..." -ForegroundColor Cyan
            & $ActivePython -m pip install --upgrade pip
            if (Test-Path "requirements.txt") { & $ActivePython -m pip install -r requirements.txt }
            Write-Host "✅ Environment Created & Ready." -ForegroundColor Green
        } else {
            Write-Host "❌ Failed to create venv." -ForegroundColor Red; exit 1
        }
    }
}

# D. UPDATE SETTINGS & EXECUTE DEPENDENCIES
if ($ActivePython) {
    if ($ActivePython -ne $JsonData.python_path) {
        $JsonData | Add-Member -Name "python_path" -Value $ActivePython -MemberType NoteProperty -Force
        $JsonData | ConvertTo-Json -Depth 4 | Set-Content $ConfigFile
    }
    $ReqScript = "check_and_install_requirements.py"
    if (Test-Path $ReqScript) {
        & $ActivePython $ReqScript
        if ($LASTEXITCODE -ne 0) { Write-Host "❌ Library check failed." -ForegroundColor Red }
    }
} else {
    $Failures += "Environment Error: Python environment could not be determined."
}

Write-Host ""

# --- 4. HELPER FUNCTIONS ---
function Add-Row {
    param ([string]$Category, [string]$Name, [string]$Path, [bool]$Found, [string]$Timestamp = "N/A")
    $StatusIcon = if ($Found) { "✅ FOUND" } else { "❌ MISSING" }
    $script:ReportData += [PSCustomObject]@{
        Status = $StatusIcon; Category = $Category; FileName = $Name; LastModified = $Timestamp; Location = $Path
    }
}

# --- 5. EXECUTE DYNAMIC FILE CHECKS ---

# A. Source Data
if ($LatestSource) {
    Add-Row -Category "1. Source Data" -Name $LatestSource.Name -Path $LatestSource.FullName -Found $true -Timestamp $LatestSource.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
}

# B. Exclusion & Training
if (Test-Path $ExclusionPath) {
    $Item = Get-Item $ExclusionPath
    Add-Row -Category "2. Process Inputs" -Name (Split-Path $ExclusionPath -Leaf) -Path $ExclusionPath -Found $true -Timestamp $Item.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
} else {
    Add-Row -Category "2. Process Inputs" -Name "Exclusion File" -Path $ExclusionPath -Found $false
    $Failures += "Missing Input: Exclusion file not found at '$ExclusionPath'."
}

if (Test-Path $TrainingFilePath) {
    $Item = Get-Item $TrainingFilePath
    Add-Row -Category "2. Process Inputs" -Name (Split-Path $TrainingFilePath -Leaf) -Path $TrainingFilePath -Found $true -Timestamp $Item.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
} else {
    Add-Row -Category "2. Process Inputs" -Name "Training File" -Path $TrainingFilePath -Found $false
    $Failures += "Missing Input: Training file not found at '$TrainingFilePath'."
}

# C. Production Models
$Models = @("ufa_identity_preprocessing.pkl", "ufa_ineligibility_preprocessing.pkl", "ufa_identity_rf.pkl", "ufa_ineligibility_gbm.pkl")
foreach ($Model in $Models) {
    $MPath = Join-Path $ProductionModels $Model
    if (Test-Path $MPath) {
        $Item = Get-Item $MPath
        Add-Row -Category "3. Prod Models" -Name $Model -Path $MPath -Found $true -Timestamp $Item.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    } else {
        Add-Row -Category "3. Prod Models" -Name $Model -Path $MPath -Found $false
        $Failures += "Missing Model: $Model not found in '$ProductionModels'."
    }
}

# D. Notebooks
$Notebooks = @("00_Run_Train_And_Process.ipynb", "01_Train_Data_Builder.ipynb", "02_Train_Identity_Model.ipynb", "03_Train_Eligibility.ipynb", "04_Train_Model_Validation.ipynb", "05_Process_Identity.ipynb", "06_Process_Enrollment.ipynb", "07_Process_Eligiblity.ipynb", "08_Process_Exclusions.ipynb")
foreach ($NB in $Notebooks) {
    $NPath = Join-Path $NotebooksDir $NB
    if (Test-Path $NPath) {
        $Item = Get-Item $NPath
        Add-Row -Category "4. Notebooks" -Name $NB -Path $NPath -Found $true -Timestamp $Item.LastWriteTime.ToString("yyyy-MM-dd HH:mm")
    } else {
        Add-Row -Category "4. Notebooks" -Name $NB -Path $NPath -Found $false
        $Failures += "Missing Notebook: $NB not found in current directory."
    }
}

# --- 6. OUTPUT: SYSTEM STATUS REPORT ---
Clear-Host
Write-Host "--- UFA SYSTEM STATUS REPORT ---" -ForegroundColor Yellow
Write-Host "(Pre-Check Run: $(Get-Date -Format 'yyyy-MM-dd HH:mm')) | (Batch Date: $($JsonData.file_date))" -ForegroundColor Gray
Write-Host ""
$ReportData | Format-Table -Property Status, FileName, LastModified, Location -GroupBy Category -AutoSize

# --- 7. OUTPUT: HISTORICAL PIVOT REFERENCE ---
Write-Host "`n--- LAST COMPLETED PIVOT SUMMARY ---" -ForegroundColor Yellow
if ($JsonData.Last_pivot_summary) {
    $HistPath = Join-Path $FinalOutputDir $JsonData.Last_pivot_summary
    if (Test-Path $HistPath) {
        Write-Host "Historical data from: " -NoNewline
        Write-Host $JsonData.Last_pivot_summary -ForegroundColor Cyan
        Write-Host "Location: $HistPath" -ForegroundColor Gray
        Write-Host "Note: This is a pre-check reference. The current batch has not been processed yet." -ForegroundColor DarkGray
    } else {
        Write-Host "⚠️ Warning: Record found in JSON but file missing at $HistPath" -ForegroundColor Yellow
    }
} else {
    Write-Host "❌ NO PREVIOUS PIVOT SUMMARY RECORDED." -ForegroundColor Red
}

# --- 8. PRE-CHECK VALIDATION SUMMARY ---
Write-Host "`n--- PRE-CHECK VALIDATION SUMMARY ---" -ForegroundColor Yellow
if ($Failures.Count -eq 0) {
    Write-Host "✅ ALL SYSTEMS GO: Ready for processing." -ForegroundColor Green
} else {
    Write-Host "❌ PRE-CHECK FAILED: Actions required before running pipeline." -ForegroundColor Red
    foreach ($F in $Failures) {
        Write-Host "  - $F" -ForegroundColor Yellow
    }
}

Write-Host "`n--- Check Complete ---" -ForegroundColor Yellow