# ============================================================
# UFA Smart Launcher - Multi-Application Launch Manager
# ============================================================
# Manages venv activation, dependency verification with pip-tools,
# application launching, and success tracking
# ============================================================

param(
    [string]$AppName = "ufa_viewer",
    [switch]$SkipDependencyCheck = $false,
    [switch]$ShowStats = $false
)

$ErrorActionPreference = "Continue"
$Script:StartTime = Get-Date

# Paths
$ScriptRoot = $PSScriptRoot
$ConfigFolder = Join-Path $ScriptRoot "smart_launcher_config"
$LogFolder = Join-Path $ScriptRoot "smart_launcher_logs"
$GuideFolder = Join-Path $ScriptRoot "Guide"

# Ensure folders exist
@($ConfigFolder, $LogFolder, $GuideFolder) | ForEach-Object {
    if (-not (Test-Path $_)) {
        New-Item -ItemType Directory -Path $_ -Force | Out-Null
    }
}

# ============================================================
# Logging Functions
# ============================================================

function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO",
        [string]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] [$Level] $Message"
    
    # Console output with color
    Write-Host $Message -ForegroundColor $Color
    
    # File output
    $logFile = Join-Path $LogFolder "smart_launcher_$(Get-Date -Format 'yyyy-MM-dd').log"
    Add-Content -Path $logFile -Value $logMessage
}

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host "  $Title" -ForegroundColor Cyan
    Write-Host ("=" * 60) -ForegroundColor Cyan
    Write-Host ""
}

# ============================================================
# Configuration Management
# ============================================================

function Get-AppConfig {
    param([string]$AppName)
    
    $configFile = Join-Path $ConfigFolder "$AppName.json"
    
    if (-not (Test-Path $configFile)) {
        Write-Log "Configuration not found for '$AppName'" "ERROR" "Red"
        Write-Log "Looking for: $configFile" "ERROR" "Red"
        return $null
    }
    
    try {
        $config = Get-Content $configFile -Raw | ConvertFrom-Json
        return $config
    } catch {
        Write-Log "Failed to parse configuration: $_" "ERROR" "Red"
        return $null
    }
}

function Update-LaunchStats {
    param(
        [string]$AppName,
        [bool]$Success,
        [string]$ErrorMessage = ""
    )
    
    $statsFile = Join-Path $LogFolder "launch_stats.json"
    
    # Load existing stats
    if (Test-Path $statsFile) {
        $stats = Get-Content $statsFile -Raw | ConvertFrom-Json
    } else {
        $stats = @{
            applications = @{}
        }
    }
    
    # Initialize app stats if needed
    if (-not $stats.applications.$AppName) {
        $stats.applications | Add-Member -NotePropertyName $AppName -NotePropertyValue @{
            total_launches = 0
            successful_launches = 0
            failed_launches = 0
            last_successful = $null
            last_failed = $null
            last_error = ""
        } -Force
    }
    
    # Update stats
    $appStats = $stats.applications.$AppName
    $appStats.total_launches++
    
    if ($Success) {
        $appStats.successful_launches++
        $appStats.last_successful = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    } else {
        $appStats.failed_launches++
        $appStats.last_failed = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        $appStats.last_error = $ErrorMessage
    }
    
    # Save stats
    $stats | ConvertTo-Json -Depth 10 | Set-Content $statsFile
}

function Show-LaunchStats {
    $statsFile = Join-Path $LogFolder "launch_stats.json"
    
    if (-not (Test-Path $statsFile)) {
        Write-Log "No launch statistics available yet" "INFO" "Yellow"
        return
    }
    
    $stats = Get-Content $statsFile -Raw | ConvertFrom-Json
    
    Write-Section "LAUNCH STATISTICS"
    
    foreach ($app in $stats.applications.PSObject.Properties) {
        $appName = $app.Name
        $appStats = $app.Value
        
        Write-Host "Application: $appName" -ForegroundColor Cyan
        Write-Host "  Total Launches:      $($appStats.total_launches)" -ForegroundColor White
        Write-Host "  Successful:          $($appStats.successful_launches)" -ForegroundColor Green
        Write-Host "  Failed:              $($appStats.failed_launches)" -ForegroundColor Red
        
        if ($appStats.last_successful) {
            Write-Host "  Last Successful:     $($appStats.last_successful)" -ForegroundColor Green
        }
        
        if ($appStats.last_failed) {
            Write-Host "  Last Failed:         $($appStats.last_failed)" -ForegroundColor Red
            if ($appStats.last_error) {
                Write-Host "  Last Error:          $($appStats.last_error)" -ForegroundColor Gray
            }
        }
        
        Write-Host ""
    }
}

# ============================================================
# Venv Management
# ============================================================

function Find-Venv {
    param([object]$Config)
    
    Write-Log "Searching for virtual environment..." "INFO" "Cyan"
    
    # Check configured venv paths
    foreach ($venvPath in $Configufa_venv.paths) {
        $fullPath = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($venvPath)
        $pythonExe = Join-Path $fullPath "Scripts\python.exe"
        
        if (Test-Path $pythonExe) {
            Write-Log "✓ Found venv: $fullPath" "SUCCESS" "Green"
            return @{
                Path = $fullPath
                Python = $pythonExe
                Activate = Join-Path $fullPath "Scripts\Activate.ps1"
            }
        }
    }
    
    Write-Log "✗ No virtual environment found" "ERROR" "Red"
    return $null
}

function Test-VenvActivated {
    return ($env:VIRTUAL_ENV -ne $null)
}

function Invoke-VenvActivation {
    param([hashtable]$VenvInfo)
    
    if (Test-VenvActivated) {
        Write-Log "Venv already activated: $env:VIRTUAL_ENV" "INFO" "Green"
        return $true
    }
    
    Write-Log "Activating virtual environment..." "INFO" "Cyan"
    
    try {
        if (Test-Path $VenvInfo.Activate) {
            & $VenvInfo.Activate
            
            # Verify activation
            if (Test-VenvActivated) {
                Write-Log "✓ Venv activated successfully" "SUCCESS" "Green"
                return $true
            }
        }
    } catch {
        Write-Log "Failed to activate venv: $_" "ERROR" "Red"
    }
    
    return $false
}

# ============================================================
# Dependency Management with pip-tools
# ============================================================

function Test-PackageInstalled {
    param(
        [string]$PythonExe,
        [string]$PackageName,
        [int]$RetryCount = 3,
        [int]$RetryDelay = 2
    )
    
    for ($i = 1; $i -le $RetryCount; $i++) {
        try {
            $result = & $PythonExe -m pip list 2>&1 | Select-String -Pattern "^$PackageName\s+" -Quiet
            
            if ($result) {
                return $true
            }
            
            if ($i -lt $RetryCount) {
                Write-Log "Package '$PackageName' not found (attempt $i/$RetryCount), retrying in ${RetryDelay}s..." "WARN" "Yellow"
                Start-Sleep -Seconds $RetryDelay
            }
        } catch {
            Write-Log "Error checking package: $_" "ERROR" "Red"
        }
    }
    
    return $false
}

function Install-PipTools {
    param(
        [string]$PythonExe,
        [bool]$WasVenvJustCreated
    )
    
    Write-Log "Checking for pip-tools..." "INFO" "Cyan"
    
    # Determine retry strategy based on whether venv was just created
    $retryCount = if ($WasVenvJustCreated) { 2 } else { 5 }
    $retryDelay = if ($WasVenvJustCreated) { 1 } else { 3 }
    
    if (Test-PackageInstalled -PythonExe $PythonExe -PackageName "pip-tools" -RetryCount $retryCount -RetryDelay $retryDelay) {
        Write-Log "✓ pip-tools already installed" "SUCCESS" "Green"
        return $true
    }
    
    Write-Log "pip-tools not found in venv, installing..." "INFO" "Yellow"
    Write-Log "This tool will sync your requirements.txt with installed packages" "INFO" "Gray"
    
    try {
        Write-Log "Running: pip install pip-tools" "INFO" "Gray"
        & $PythonExe -m pip install --upgrade pip-tools 2>&1 | Out-Null
        
        # Verify installation with extended retry for new installs
        if (Test-PackageInstalled -PythonExe $PythonExe -PackageName "pip-tools" -RetryCount 5 -RetryDelay 3) {
            Write-Log "✓ pip-tools installed successfully" "SUCCESS" "Green"
            return $true
        } else {
            Write-Log "✗ pip-tools installation could not be verified" "ERROR" "Red"
            return $false
        }
    } catch {
        Write-Log "Failed to install pip-tools: $_" "ERROR" "Red"
        return $false
    }
}

function Sync-Requirements {
    param(
        [string]$PythonExe,
        [string]$RequirementsFile
    )
    
    if (-not (Test-Path $RequirementsFile)) {
        Write-Log "Requirements file not found: $RequirementsFile" "ERROR" "Red"
        return $false
    }
    
    Write-Log "Syncing requirements with pip-sync..." "INFO" "Cyan"
    Write-Log "Requirements file: $RequirementsFile" "INFO" "Gray"
    
    try {
        # Run pip-sync to ensure all requirements are met
        $output = & $PythonExe -m piptools sync $RequirementsFile 2>&1
        
        Write-Log "pip-sync output:" "INFO" "Gray"
        $output | ForEach-Object { Write-Log "  $_" "INFO" "DarkGray" }
        
        Write-Log "✓ Requirements synchronized" "SUCCESS" "Green"
        return $true
    } catch {
        Write-Log "Failed to sync requirements: $_" "ERROR" "Red"
        return $false
		}
}

# ============================================================
# Application Launch
# ============================================================

function Start-Application {
    param(
        [string]$PythonExe,
        [string]$ScriptPath,
        [array]$Arguments,
        [string]$ProcessName
    )
    
    Write-Log "Launching application..." "INFO" "Cyan"
    Write-Log "Command: $PythonExe $ScriptPath $($Arguments -join ' ')" "INFO" "Gray"
    
    try {
        $process = Start-Process -FilePath $PythonExe -ArgumentList @($ScriptPath) + $Arguments -PassThru -NoNewWindow:$false
        
        # Wait a moment for process to initialize
        Start-Sleep -Seconds 2
        
        # Check if process is running
        if ($process -and -not $process.HasExited) {
            Write-Log "✓ Application started successfully (PID: $($process.Id))" "SUCCESS" "Green"
            return $true
        } else {
            Write-Log "✗ Application process exited immediately" "ERROR" "Red"
            return $false
        }
    } catch {
        Write-Log "Failed to start application: $_" "ERROR" "Red"
        return $false
    }
}

function Test-ApplicationRunning {
    param([string]$ProcessName)
    
    if (-not $ProcessName) {
        return $null
    }
    
    $processes = Get-Process -Name $ProcessName -ErrorAction SilentlyContinue
    return ($processes -ne $null -and $processes.Count -gt 0)
}

# ============================================================
# Main Execution
# ============================================================

function Start-SmartLauncher {
    param(
        [string]$AppName,
        [bool]$SkipDeps
    )
    
    Write-Section "UFA SMART LAUNCHER"
    Write-Log "Application: $AppName" "INFO" "Cyan"
    Write-Log "Start Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" "INFO" "Gray"
    Write-Host ""
    
    # Load configuration
    $config = Get-AppConfig -AppName $AppName
    if (-not $config) {
        Update-LaunchStats -AppName $AppName -Success $false -ErrorMessage "Configuration not found"
        return $false
    }
    
    # Find and activate venv
    $venv = Find-Venv -Config $config
    if (-not $venv) {
        $errorMsg = "Virtual environment not found at configured paths"
        Write-Log $errorMsg "ERROR" "Red"
        Update-LaunchStats -AppName $AppName -Success $false -ErrorMessage $errorMsg
        return $false
    }
    
    # Activate venv if not already activated
    if (-not (Test-VenvActivated)) {
        if (-not (Invoke-VenvActivation -VenvInfo $venv)) {
            # Even if activation fails, we can still use the Python exe directly
            Write-Log "Continuing with direct Python executable usage" "WARN" "Yellow"
        }
    }
    
    # Dependency management
    if (-not $SkipDeps) {
        Write-Host ""
        Write-Section "DEPENDENCY MANAGEMENT"
        
        # Install pip-tools if needed
        $wasVenvNew = -not (Test-Path (Join-Path $venv.Path "Lib\site-packages"))
        if (-not (Install-PipTools -PythonExe $venv.Python -WasVenvJustCreated $wasVenvNew)) {
            $errorMsg = "Failed to install pip-tools"
            Write-Log $errorMsg "ERROR" "Red"
            Update-LaunchStats -AppName $AppName -Success $false -ErrorMessage $errorMsg
            return $false
        }
        
        # Sync requirements
        foreach ($reqFile in $config.requirements.files) {
            $fullPath = Join-Path $ScriptRoot $reqFile
            if (Test-Path $fullPath) {
                if (-not (Sync-Requirements -PythonExe $venv.Python -RequirementsFile $fullPath)) {
                    Write-Log "Warning: Failed to sync $reqFile" "WARN" "Yellow"
                }
            }
        }
    } else {
        Write-Log "Skipping dependency check (as requested)" "INFO" "Yellow"
    }
    
    # Launch application
    Write-Host ""
    Write-Section "APPLICATION LAUNCH"
    
    $scriptPath = Join-Path $ScriptRoot $config.application.script
    $success = Start-Application -PythonExe $venv.Python -ScriptPath $scriptPath -Arguments $config.application.arguments -ProcessName $config.application.process_name
    
    if ($success) {
        # Check if process is actually running
        if ($config.application.process_name) {
            Start-Sleep -Seconds 2
            $isRunning = Test-ApplicationRunning -ProcessName $config.application.process_name
            if ($isRunning) {
                Write-Log "✓ Application is running" "SUCCESS" "Green"
            } else {
                Write-Log "⚠ Application may have exited" "WARN" "Yellow"
            }
        }
        
        Update-LaunchStats -AppName $AppName -Success $true
        
        $elapsed = (Get-Date) - $Script:StartTime
        Write-Host ""
        Write-Log "Launch completed successfully in $($elapsed.TotalSeconds) seconds" "SUCCESS" "Green"
        return $true
    } else {
        $errorMsg = "Application failed to start"
        Update-LaunchStats -AppName $AppName -Success $false -ErrorMessage $errorMsg
        Write-Log $errorMsg "ERROR" "Red"
        return $false
    }
}

# ============================================================
# Entry Point
# ============================================================

if ($ShowStats) {
    Show-LaunchStats
    exit 0
}

$success = Start-SmartLauncher -AppName $AppName -SkipDeps $SkipDependencyCheck

if ($success) {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Green
    Write-Host "  LAUNCH SUCCESSFUL" -ForegroundColor Green
    Write-Host ("=" * 60) -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host ("=" * 60) -ForegroundColor Red
    Write-Host "  LAUNCH FAILED" -ForegroundColor Red
    Write-Host ("=" * 60) -ForegroundColor Red
    Write-Host ""
    Write-Host "Check logs in: $LogFolder" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}
