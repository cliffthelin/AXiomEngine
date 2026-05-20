<#
.SYNOPSIS
    UFA Pipeline Pre-Flight Validation Script
    
.DESCRIPTION
    Validates environment, files, and configuration before running the UFA pipeline.
    Returns exit code 0 on success, non-zero on failure.
    
.PARAMETER ConfigPath
    Path to appsettings.json configuration file
    
.PARAMETER LogPath
    Path to write validation log
    
.PARAMETER WarningsAsErrors
    Treat warnings as errors (fail validation on warnings)
    
.EXAMPLE
    .\UFA_Pipeline_Precheck.ps1 -ConfigPath "appsettings.json" -LogPath "run_logs\precheck.log"
#>

param(
    [Parameter(Mandatory=$false)]
    [string]$ConfigPath = "appsettings.json",
    
    [Parameter(Mandatory=$false)]
    [string]$LogPath = "run_logs\precheck_$(Get-Date -Format 'yyyyMMdd_HHmmss').log",
    
    [Parameter(Mandatory=$false)]
    [switch]$WarningsAsErrors = $false
)

# Initialize
$ErrorActionPreference = "Continue"
$Script:ValidationErrors = @()
$Script:ValidationWarnings = @()
$Script:StartTime = Get-Date

# Ensure log directory exists
$logDir = Split-Path -Path $LogPath -Parent
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Logging function
function Write-ValidationLog {
    param(
        [string]$Message,
        [ValidateSet('INFO', 'SUCCESS', 'WARNING', 'ERROR')]
        [string]$Level = 'INFO'
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $prefix = switch ($Level) {
        'SUCCESS' { '✅' }
        'WARNING' { '⚠️ ' }
        'ERROR'   { '❌' }
        default   { 'ℹ️ ' }
    }
    
    $logLine = "[$timestamp] [$Level] $Message"
    $consoleLine = "$prefix $Message"
    
    # Write to console with color
    switch ($Level) {
        'SUCCESS' { Write-Host $consoleLine -ForegroundColor Green }
        'WARNING' { Write-Host $consoleLine -ForegroundColor Yellow }
        'ERROR'   { Write-Host $consoleLine -ForegroundColor Red }
        default   { Write-Host $consoleLine }
    }
    
    # Append to log file
    Add-Content -Path $LogPath -Value $logLine
}

# Add validation error
function Add-ValidationError {
    param([string]$Message)
    $Script:ValidationErrors += $Message
    Write-ValidationLog -Message $Message -Level 'ERROR'
}

# Add validation warning
function Add-ValidationWarning {
    param([string]$Message)
    $Script:ValidationWarnings += $Message
    Write-ValidationLog -Message $Message -Level 'WARNING'
}

# Main validation
try {
    Write-ValidationLog -Message "======================================================================"
    Write-ValidationLog -Message "🚦 UFA PIPELINE PRE-FLIGHT VALIDATION"
    Write-ValidationLog -Message "======================================================================"
    Write-ValidationLog -Message ""
    
    # ============================================================
    # CHECK 1: Configuration File
    # ============================================================
    Write-ValidationLog -Message "[1/10] Validating configuration file..."
    
    if (-not (Test-Path $ConfigPath)) {
        Add-ValidationError "Configuration file not found: $ConfigPath"
        throw "Cannot proceed without configuration file"
    }
    
    try {
        $config = Get-Content $ConfigPath -Raw | ConvertFrom-Json
        Write-ValidationLog -Message "Configuration loaded successfully" -Level 'SUCCESS'
    } catch {
        Add-ValidationError "Configuration file is not valid JSON: $_"
        throw "Invalid configuration file"
    }
    
    # ============================================================
    # CHECK 2: Required Configuration Keys
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[2/10] Validating required configuration keys..."
    
    $requiredKeys = @(
        'file_date',
        'code_ready_ufa_file_name',
        'ufa_file_name',
        'created_files',
        'final_output',
        'ufa_files',
        'ml_models',
        'exclusion_file',
        'python_path',
        'jupyter_kernel_name'
    )
    
    foreach ($key in $requiredKeys) {
        if (-not $config.PSObject.Properties.Name.Contains($key)) {
            Add-ValidationError "Required config key missing: '$key'"
        } elseif ([string]::IsNullOrWhiteSpace($config.$key)) {
            Add-ValidationError "Required config key is empty: '$key'"
        } else {
            Write-ValidationLog -Message "   ✅ $key" -Level 'INFO'
        }
    }
    
    # ============================================================
    # CHECK 3: Processing Notebooks Exist
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[3/10] Validating notebook chain..."
    
    $requiredNotebooks = @(
        '05_Process_Identity.ipynb',
        '06_Process_Enrollment.ipynb',
        '07_Process_Eligibility.ipynb',
        '08_Process_Exclusions.ipynb',
        '09_Final_Reporting.ipynb'
    )
    
    foreach ($notebook in $requiredNotebooks) {
        if (-not (Test-Path $notebook)) {
            Add-ValidationError "Required notebook missing: $notebook"
        } else {
            Write-ValidationLog -Message "   ✅ $notebook" -Level 'INFO'
        }
    }
    
    # ============================================================
    # CHECK 4: Output Directories Writable
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[4/10] Validating output directories..."
    
    $criticalDirs = @{
        'Created Files' = $config.created_files
        'Final Output' = $config.final_output
        'UFA Files' = $config.ufa_files
        'ML Models' = $config.ml_models
    }
    
    foreach ($dirLabel in $criticalDirs.Keys) {
        $dirPath = $criticalDirs[$dirLabel]
        
        # Create directory if it doesn't exist
        if (-not (Test-Path $dirPath)) {
            try {
                New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
                Write-ValidationLog -Message "   Created: $dirLabel at $dirPath" -Level 'INFO'
            } catch {
                Add-ValidationError "$dirLabel directory cannot be created: $dirPath ($_)"
                continue
            }
        }
        
        # Test writability
        $testFile = Join-Path $dirPath ".write_test_$(Get-Date -Format 'yyyyMMddHHmmss').tmp"
        try {
            "test" | Out-File -FilePath $testFile -Force
            Remove-Item -Path $testFile -Force
            Write-ValidationLog -Message "   ✅ $dirLabel : $dirPath" -Level 'INFO'
        } catch {
            Add-ValidationError "$dirLabel not writable: $dirPath ($_)"
        }
    }
    
    # ============================================================
    # CHECK 5: Production Models Exist (if not retraining)
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[5/10] Validating ML models..."
    
    $forceRetrain = $config.force_retrain -eq $true
    $retrainMode = $config.retrain_mode -eq $true
    
    if ($forceRetrain -or $retrainMode) {
        Write-ValidationLog -Message "   ℹ️  Retraining mode - models will be created" -Level 'INFO'
    } else {
        $modelDir = Join-Path $config.ml_models "production"
        $requiredModels = @(
            'ufa_identity_stacking.pkl',
            'ufa_ineligibility_stacking.pkl',
            'nn_model_identity.keras',
            'nn_model_ineligibility.keras'
        )
        
        foreach ($model in $requiredModels) {
            $modelPath = Join-Path $modelDir $model
            if (-not (Test-Path $modelPath)) {
                Add-ValidationError "Production model missing: $model at $modelPath"
            } else {
                Write-ValidationLog -Message "   ✅ $model" -Level 'INFO'
            }
        }
    }
    
    # ============================================================
    # CHECK 6: Notebook 05 Input Files
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[6/10] Validating Notebook 05 inputs..."
    
    $fileDate = $config.file_date
    $createdFiles = $config.created_files
    
    $nb05Files = @(
        @{Path = Join-Path $createdFiles "02_ml_data_$fileDate.csv"; Label = "ML Data"}
        @{Path = Join-Path $createdFiles "final_df_$fileDate.csv"; Label = "Final DataFrame"}
    )
    
    foreach ($file in $nb05Files) {
        if (-not (Test-Path $file.Path)) {
            Add-ValidationError "NB05 input missing: $($file.Label) at $($file.Path)"
        } else {
            Write-ValidationLog -Message "   ✅ $($file.Label)" -Level 'INFO'
        }
    }
    
    # ============================================================
    # CHECK 7: UFA Input File
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[7/10] Validating UFA input file..."
    
    $ufaFilePath = Join-Path $config.ufa_files $config.ufa_file_name
    if (-not (Test-Path $ufaFilePath)) {
        Add-ValidationError "UFA input file not found: $ufaFilePath"
    } else {
        $fileSize = (Get-Item $ufaFilePath).Length / 1MB
        $fileSizeStr = $fileSize.ToString('F2') + ' MB'
        Write-ValidationLog -Message "   ✅ UFA file found: $($config.ufa_file_name) ($fileSizeStr)" -Level 'SUCCESS'
    }
    
    # ============================================================
    # CHECK 8: Exclusion File
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[8/10] Validating exclusion file..."
    
    $exclusionFile = $config.exclusion_file
    if (-not (Test-Path $exclusionFile)) {
        Add-ValidationWarning "Exclusion file not found: $exclusionFile"
    } else {
        Write-ValidationLog -Message "   ✅ Exclusion file found: $exclusionFile" -Level 'SUCCESS'
    }
    
    # ============================================================
    # CHECK 9: Jupyter Kernel
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[9/10] Validating Jupyter kernel..."
    
    try {
        # Try to find jupyter executable
        $jupyterCmd = Get-Command jupyter -ErrorAction SilentlyContinue
        
        if (-not $jupyterCmd) {
            # Jupyter not in PATH - try to use Python from config to find it
            if ($config.python_path) {
                $pythonDir = Split-Path -Parent $config.python_path
                $jupyterExe = Join-Path $pythonDir "jupyter.exe"
                
                if (Test-Path $jupyterExe) {
                    $kernelList = & $jupyterExe kernelspec list 2>&1 | Out-String
                } else {
                    throw "Jupyter not found in PATH or at $jupyterExe"
                }
            } else {
                throw "Jupyter not found in PATH and no python_path configured"
            }
        } else {
            $kernelList = & jupyter kernelspec list 2>&1 | Out-String
        }
        
        $kernelName = $config.jupyter_kernel_name
        
        if ($kernelList -match $kernelName) {
            Write-ValidationLog -Message "   ✅ Jupyter kernel '$kernelName' is installed" -Level 'SUCCESS'
        } else {
            Add-ValidationError "Jupyter kernel '$kernelName' not found. Run: jupyter kernelspec list"
            Write-ValidationLog -Message "   Available kernels:" -Level 'INFO'
            Write-ValidationLog -Message $kernelList -Level 'INFO'
        }
    } catch {
        Add-ValidationWarning "Cannot verify Jupyter kernel (jupyter command not found): $_"
        Write-ValidationLog -Message "   Skipping kernel check - will be verified during notebook execution" -Level 'INFO'
    }
    
    # ============================================================
    # CHECK 10: Disk Space
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "[10/10] Validating disk space..."
    
    try {
        $drive = (Get-Location).Drive
        $freeGB = [math]::Round($drive.Free / 1GB, 2)
        $totalGB = [math]::Round(($drive.Used + $drive.Free) / 1GB, 2)
        $usedPct = [math]::Round(($drive.Used / ($drive.Used + $drive.Free)) * 100, 1)
        
        Write-ValidationLog -Message "   📊 Disk: $freeGB GB free / $totalGB GB total ($usedPct% used)" -Level 'INFO'
        
        if ($freeGB -lt 1.0) {
            Add-ValidationError "Critical: Low disk space ($freeGB GB free). Pipeline may fail."
        } elseif ($freeGB -lt 5.0) {
            Add-ValidationWarning "Low disk space: $freeGB GB free. Consider freeing space."
        } else {
            Write-ValidationLog -Message "   ✅ Sufficient disk space available" -Level 'SUCCESS'
        }
    } catch {
        Add-ValidationWarning "Could not check disk space: $_"
    }
    
    # ============================================================
    # FINAL VALIDATION SUMMARY
    # ============================================================
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "======================================================================"
    
    $elapsed = ((Get-Date) - $Script:StartTime).TotalSeconds
    
    if ($Script:ValidationErrors.Count -gt 0) {
        Write-ValidationLog -Message "❌ PRE-FLIGHT VALIDATION FAILED" -Level 'ERROR'
        Write-ValidationLog -Message "======================================================================"
        Write-ValidationLog -Message ""
        Write-ValidationLog -Message "🚨 CRITICAL ERRORS (must be fixed before proceeding):" -Level 'ERROR'
        Write-ValidationLog -Message ""
        
        for ($i = 0; $i -lt $Script:ValidationErrors.Count; $i++) {
            Write-ValidationLog -Message "   $($i + 1). $($Script:ValidationErrors[$i])" -Level 'ERROR'
        }
        
        if ($Script:ValidationWarnings.Count -gt 0) {
            Write-ValidationLog -Message ""
            Write-ValidationLog -Message "⚠️  WARNINGS (review recommended):" -Level 'WARNING'
            Write-ValidationLog -Message ""
            
            for ($i = 0; $i -lt $Script:ValidationWarnings.Count; $i++) {
                Write-ValidationLog -Message "   $($i + 1). $($Script:ValidationWarnings[$i])" -Level 'WARNING'
            }
        }
        
        Write-ValidationLog -Message ""
        Write-ValidationLog -Message "======================================================================"
        Write-ValidationLog -Message "Validation completed in $([math]::Round($elapsed, 2)) seconds" -Level 'INFO'
        Write-ValidationLog -Message "Pre-flight validation failed with $($Script:ValidationErrors.Count) error(s)."
        Write-ValidationLog -Message "📂 Full log: $LogPath"
        Write-ValidationLog -Message ""
        
        exit 1
        
    } elseif ($Script:ValidationWarnings.Count -gt 0) {
        if ($WarningsAsErrors) {
            Write-ValidationLog -Message "❌ PRE-FLIGHT VALIDATION FAILED (WARNINGS AS ERRORS)" -Level 'ERROR'
            Write-ValidationLog -Message "======================================================================"
            Write-ValidationLog -Message ""
            
            for ($i = 0; $i -lt $Script:ValidationWarnings.Count; $i++) {
                Write-ValidationLog -Message "   $($i + 1). $($Script:ValidationWarnings[$i])" -Level 'WARNING'
            }
            
            Write-ValidationLog -Message ""
            Write-ValidationLog -Message "======================================================================"
            Write-ValidationLog -Message "Validation completed in $([math]::Round($elapsed, 2)) seconds" -Level 'INFO'
            Write-ValidationLog -Message "Pre-flight validation failed with $($Script:ValidationWarnings.Count) warning(s)."
            Write-ValidationLog -Message "📂 Full log: $LogPath"
            Write-ValidationLog -Message ""
            
            exit 1
        } else {
            Write-ValidationLog -Message "⚠️  PRE-FLIGHT VALIDATION PASSED WITH WARNINGS" -Level 'WARNING'
            Write-ValidationLog -Message "======================================================================"
            Write-ValidationLog -Message ""
            Write-ValidationLog -Message "⚠️  WARNINGS (pipeline will proceed, but review recommended):" -Level 'WARNING'
            Write-ValidationLog -Message ""
            
            for ($i = 0; $i -lt $Script:ValidationWarnings.Count; $i++) {
                Write-ValidationLog -Message "   $($i + 1). $($Script:ValidationWarnings[$i])" -Level 'WARNING'
            }
            
            Write-ValidationLog -Message ""
            Write-ValidationLog -Message "======================================================================"
            Write-ValidationLog -Message "Validation completed in $([math]::Round($elapsed, 2)) seconds" -Level 'INFO'
            Write-ValidationLog -Message "✅ All critical checks passed. Proceeding with caution..."
            Write-ValidationLog -Message "📂 Full log: $LogPath"
            Write-ValidationLog -Message ""
            
            exit 0
        }
        
    } else {
        Write-ValidationLog -Message "✅ PRE-FLIGHT VALIDATION PASSED" -Level 'SUCCESS'
        Write-ValidationLog -Message "======================================================================"
        Write-ValidationLog -Message ""
        Write-ValidationLog -Message "Validation completed in $([math]::Round($elapsed, 2)) seconds" -Level 'INFO'
        Write-ValidationLog -Message "All systems go! Pipeline is ready for execution." -Level 'SUCCESS'
        Write-ValidationLog -Message "📂 Full log: $LogPath"
        Write-ValidationLog -Message ""
        
        exit 0
    }
    
} catch {
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "======================================================================"
    Write-ValidationLog -Message "❌ FATAL ERROR DURING VALIDATION" -Level 'ERROR'
    Write-ValidationLog -Message "======================================================================"
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "Error: $_" -Level 'ERROR'
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "Stack Trace:" -Level 'ERROR'
    Write-ValidationLog -Message $_.ScriptStackTrace -Level 'ERROR'
    Write-ValidationLog -Message ""
    Write-ValidationLog -Message "======================================================================"
    Write-ValidationLog -Message "📂 Full log: $LogPath"
    Write-ValidationLog -Message ""
    
    exit 2
}
