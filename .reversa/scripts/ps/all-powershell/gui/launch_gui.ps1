# UFA Pipeline Viewer - Smart Launcher
# Checks prerequisites and guides setup if needed

# Ensure console stays visible even on errors
$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  UFA USBE Cross Enrollment - Smart Launch  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "[DEBUG] Launcher started at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor DarkGray
Write-Host ""

# Step 0: Dependency Validation (optional - only if validate_dependencies.py exists)
# This validator checks actual imports in your code vs requirements.txt
# Set skip_validation: true in launcher_config.json to disable this check
if ((Test-Path "validate_dependencies.py") -and (Get-Command python -ErrorAction SilentlyContinue)) {
    # Check if user wants validation (from launcher_config.json)
    $configPath = "launcher_config.json"
    if (Test-Path $configPath) {
        try {
            $config = Get-Content $configPath -Raw | ConvertFrom-Json
            $skipValidation = $config.validation_settings.skip_validation
            
            if ($skipValidation -eq $true) {
                Write-Host "[0/5] ⏭️  Dependency validation skipped (configured)" -ForegroundColor DarkGray
                Write-Host ""
            } else {
                Write-Host "[0/5] Running dependency validator..." -ForegroundColor Cyan
                Write-Host "      Checking if installed packages match code requirements" -ForegroundColor DarkGray
                Write-Host ""
                
                # Determine which Python to use - MUST use the external venv with all packages
                # ALWAYS use the full path to the external venv - never rely on PATH or local ufa_venv
                $validatorPython = "c:\Users\Cliff.Thelin\Source\ufa\ufa_venv\Scripts\python.exe"
                
                if (Test-Path $validatorPython) {
                    Write-Host "      Using external venv Python for validation" -ForegroundColor DarkGray
                } elseif (Test-Path "ufa_venv\Scripts\python.exe") {
                    # Use local venv as fallback
                    $validatorPython = ".\ufa_venv\Scripts\python.exe"
                    Write-Host "      Using local ufa_venv Python for validation" -ForegroundColor DarkGray
                } else {
                    Write-Host "      Using system Python (venv not found)" -ForegroundColor Yellow
                }
                
                try {
                    & $validatorPython validate_dependencies.py
                    $validatorExitCode = $LASTEXITCODE
                    
                    if ($validatorExitCode -ne 0) {
                        Write-Host ""
                        Write-Host "========================================" -ForegroundColor Yellow
                        Write-Host "[!] DEPENDENCY VALIDATION ISSUES" -ForegroundColor Yellow
                        Write-Host "========================================" -ForegroundColor Yellow
                        Write-Host ""
                        Write-Host "Some packages may need attention. Check output above." -ForegroundColor Yellow
                        Write-Host ""
                        
                        $response = Read-Host "Continue anyway? (Y/N)"
                        if ($response -notmatch '^[Yy]') {
                            Write-Host ""
                            Write-Host "Launch cancelled. Fix validation issues and try again." -ForegroundColor Red
                            Write-Host ""
                            Read-Host "Press Enter to exit"
                            exit 1
                        }
                        Write-Host ""
                        Write-Host "[!] Continuing despite validation issues..." -ForegroundColor Yellow
                    } else {
                        Write-Host "[OK] ✓ Dependencies validated" -ForegroundColor Green
                    }
                } catch {
                    Write-Host "[!] Could not run dependency validator: $_" -ForegroundColor Yellow
                }
                Write-Host ""
            }
        } catch {
            Write-Host "[WARNING] Could not read validation settings from config" -ForegroundColor Yellow
        }
    }
}

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) { return $true }
    } catch {
        return $false
    }
}

# Function to check if packages are installed
function Test-PythonPackages {
    param($Packages)
    try {
        foreach ($pkg in $Packages) {
            $check = python -c "import $pkg" 2>&1
            if ($LASTEXITCODE -ne 0) {
                return $false
            }
        }
        return $true
    } catch {
        return $false
    }
}

# Function to prompt user
function Get-UserConfirmation {
    param($Message)
    Write-Host ""
    Write-Host $Message -ForegroundColor Yellow
    $response = Read-Host "Proceed? (Y/N)"
    return ($response -eq "Y" -or $response -eq "y")
}

# Function to wait for process completion
function Wait-ForSetup {
    param($ProcessName)
    Write-Host ""
    Write-Host "Setup in progress... Checking every 60 seconds..." -ForegroundColor Cyan
    while ($true) {
        Start-Sleep -Seconds 60
        Write-Host "Checking if setup is complete..." -ForegroundColor Gray
        # Re-check the condition
        return
    }
}

Write-Host "🔍 Checking prerequisites..." -ForegroundColor Cyan
Write-Host ""

$setupNeeded = $false
$hasEmailFormatter = $false
$hasDataFiles = $false

# Step 1: Check Python
Write-Host "[1/5] " -NoNewline
if (Test-Command python) {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is installed ($pythonVersion)" -ForegroundColor Green
} else {
    Write-Host "✗ Python is NOT installed" -ForegroundColor Red
    Write-Host "    Please install Python from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "    Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Step 2: Check Virtual Environment
Write-Host "[2/5] " -NoNewline
if (Test-Path "ufa_venv\Scripts\Activate.ps1") {
    Write-Host "✓ Virtual environment exists" -ForegroundColor Green
    $hasVenv = $true
} else {
    Write-Host "✗ Virtual environment not found" -ForegroundColor Red
    $hasVenv = $false
    $setupNeeded = $true
}

# Step 3: Check Required Packages (if venv exists, activate and check)
Write-Host "[3/5] " -NoNewline
if ($hasVenv) {
    # Use venv Python directly instead of relying on activation
    $venvPython = ".\ufa_venv\Scripts\python.exe"
    
    Write-Host "" # newline
    Write-Host "      Testing with: $venvPython" -ForegroundColor DarkGray
    
    # Test imports with the actual Python executable that will be used
    # Only check packages actually needed by the GUI
    $testImport = & $venvPython -c "import customtkinter, pandas, tkinter; print('OK')" 2>&1
    
    if ($testImport -match "OK") {
        Write-Host "      ✓ Required GUI packages are installed" -ForegroundColor Green
        $packagesInstalled = $true
    } else {
        Write-Host "      ✗ Required GUI packages are missing" -ForegroundColor Red
        Write-Host "      Missing: customtkinter, pandas, or tkinter" -ForegroundColor Gray
        $packagesInstalled = $false
        $setupNeeded = $true
    }
} else {
    Write-Host "⊘ Skipped (no virtual environment)" -ForegroundColor Yellow
    Write-Host "      Packages cannot be checked without venv" -ForegroundColor Gray
    $packagesInstalled = $false
}

# Step 4: Check email_formatter.py
Write-Host "[4/5] " -NoNewline
if (Test-Path "email_formatter.py") {
    Write-Host "✓ Email formatter module found" -ForegroundColor Green
    $hasEmailFormatter = $true
} else {
    Write-Host "✗ Email formatter module missing" -ForegroundColor Red
    Write-Host "      This file is required for email generation features" -ForegroundColor Yellow
    $hasEmailFormatter = $false
    $setupNeeded = $true
}

# Step 5: Check final_output folder
Write-Host "[5/5] " -NoNewline
if (Test-Path "final_output") {
    $csvFiles = @(Get-ChildItem "final_output\Cross-Enrolled-*.csv" -ErrorAction SilentlyContinue)
    if ($csvFiles.Count -gt 0) {
        Write-Host "✓ Data folder exists with $($csvFiles.Count) file(s)" -ForegroundColor Green
        $hasDataFiles = $true
    } else {
        Write-Host "⚠ Data folder exists but no CSV files found" -ForegroundColor Yellow
        Write-Host "      File tab will be empty until pipeline runs" -ForegroundColor Gray
        $hasDataFiles = $false
    }
} else {
    Write-Host "⚠ Data folder not found" -ForegroundColor Yellow
    Write-Host "      Will be created automatically" -ForegroundColor Gray
    $hasDataFiles = $false
}

Write-Host ""
Write-Host ("=" * 50) -ForegroundColor Gray
Write-Host ""

# If setup needed, guide user through it
if ($setupNeeded) {
    Write-Host "⚙️  SETUP REQUIRED" -ForegroundColor Yellow
    Write-Host ""
    
    # Setup Virtual Environment
    if (-not $hasVenv) {
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host "📦 Virtual Environment Setup" -ForegroundColor Cyan
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "A virtual environment creates an isolated space for this" -ForegroundColor White
        Write-Host "application's Python packages. This ensures:" -ForegroundColor White
        Write-Host "  • No conflicts with other Python software on your system" -ForegroundColor Gray
        Write-Host "  • Easy package management for this project only" -ForegroundColor Gray
        Write-Host "  • Clean separation from system-wide Python installation" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Recommended: This will NOT affect any other software." -ForegroundColor Green
        
        if (Get-UserConfirmation "Create virtual environment?") {
            Write-Host ""
            Write-Host "Creating virtual environment..." -ForegroundColor Cyan
            python -m venv ufa_venv
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green
                $hasVenv = $true
                # After creating venv, packages will need to be installed
                $packagesInstalled = $false
            } else {
                Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
                Write-Host ""
                Write-Host "Press any key to exit..." -ForegroundColor Gray
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                exit 1
            }
        } else {
            Write-Host ""
            Write-Host "Setup cancelled. Cannot proceed without virtual environment." -ForegroundColor Red
            Write-Host ""
            Write-Host "Press any key to exit..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
    
    # Install Required Packages
    if (-not $packagesInstalled) {
        Write-Host ""
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host "📚 Package Installation" -ForegroundColor Cyan
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
        Write-Host ""
        Write-Host "Required packages:" -ForegroundColor White
        Write-Host "  • customtkinter - Modern GUI framework" -ForegroundColor Gray
        Write-Host "  • pandas         - Data processing" -ForegroundColor Gray
        Write-Host "  • pillow         - Image handling" -ForegroundColor Gray
        Write-Host ""
        Write-Host "These will be installed in the virtual environment only." -ForegroundColor Green
        
        if (Get-UserConfirmation "Install required packages?") {
            Write-Host ""
            Write-Host "Installing packages (this may take 1-2 minutes)..." -ForegroundColor Cyan
            
            # Use venv Python directly if available
            if (Test-Path "ufa_venv\Scripts\python.exe") {
                Write-Host "Installing to virtual environment..." -ForegroundColor Gray
                & .\ufa_venv\Scripts\python.exe -m pip install --upgrade pip -q
                & .\ufa_venv\Scripts\python.exe -m pip install customtkinter pandas pillow -q
            } else {
                python -m pip install --upgrade pip -q
                python -m pip install customtkinter pandas pillow -q
            }
            
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Packages installed successfully" -ForegroundColor Green
                $packagesInstalled = $true
            } else {
                Write-Host "✗ Failed to install packages" -ForegroundColor Red
                Write-Host ""
                Write-Host "Try running manually:" -ForegroundColor Yellow
                Write-Host "  .\ufa_venv\Scripts\Activate.ps1" -ForegroundColor Gray
                Write-Host "  pip install customtkinter pandas pillow" -ForegroundColor Gray
                Write-Host ""
                Write-Host "Press any key to exit..." -ForegroundColor Gray
                $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
                exit 1
            }
        } else {
            Write-Host ""
            Write-Host "Setup cancelled. Cannot proceed without required packages." -ForegroundColor Red
            Write-Host ""
            Write-Host "Press any key to exit..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    }
    
    Write-Host ""
    Write-Host ("=" * 50) -ForegroundColor Gray
    Write-Host ""
}

# Handle missing email_formatter.py
if (-not $hasEmailFormatter) {
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "⚠️  Missing Email Formatter" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    Write-Host "The email_formatter.py file is required for the email" -ForegroundColor White
    Write-Host "generation feature (Email Response tab)." -ForegroundColor White
    Write-Host ""
    Write-Host "This file should be in the same folder as ufa_pipeline_viewer.py" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  1. Restore from backup if available" -ForegroundColor Gray
    Write-Host "  2. Recreate from documentation" -ForegroundColor Gray
    Write-Host "  3. Continue anyway (Email tab will not work)" -ForegroundColor Gray
    Write-Host ""
    
    if (Get-UserConfirmation "Continue launching without email formatter?") {
        Write-Host ""
        Write-Host "⚠ Continuing without email formatter" -ForegroundColor Yellow
        Write-Host "   The Email Response tab may show errors" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "Launch cancelled. Please restore email_formatter.py and try again." -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

# Handle missing data folder
if (-not $hasDataFiles) {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host "📁 Data Folder Setup" -ForegroundColor Cyan
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
    Write-Host ""
    
    if (-not (Test-Path "final_output")) {
        Write-Host "Creating final_output folder..." -ForegroundColor Cyan
        New-Item -ItemType Directory -Path "final_output" -Force | Out-Null
        Write-Host "✓ Folder created" -ForegroundColor Green
        Write-Host ""
    }
    
    Write-Host "The final_output folder is where pipeline data files are stored." -ForegroundColor White
    Write-Host "The File tab will show historical runs from this folder." -ForegroundColor White
    Write-Host ""
    Write-Host "Current status: No CSV files found" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This is normal if:" -ForegroundColor Gray
    Write-Host "  • First time running the application" -ForegroundColor Gray
    Write-Host "  • Pipeline hasn't been executed yet" -ForegroundColor Gray
    Write-Host "  • Files are in a different location" -ForegroundColor Gray
    Write-Host ""
    Write-Host "You can still:" -ForegroundColor Green
    Write-Host "  • Use the Student lookup features" -ForegroundColor Gray
    Write-Host "  • The File tab will populate after pipeline runs" -ForegroundColor Gray
    Write-Host ""
}

if ($setupNeeded) {
    Write-Host ("=" * 50) -ForegroundColor Gray
    Write-Host ""
    Write-Host "✓ Setup complete!" -ForegroundColor Green
    Write-Host ""
}

# Final check and launch
Write-Host "🚀 Launching UFA USBE Cross Enrollment..." -ForegroundColor Green
Write-Host ""

# Verify the Python file exists
Write-Host "[DEBUG] Checking for ufa_pipeline_viewer.py..." -ForegroundColor DarkGray
if (-not (Test-Path "ufa_pipeline_viewer.py")) {
    Write-Host "✗ ERROR: ufa_pipeline_viewer.py not found!" -ForegroundColor Red
    Write-Host "    Current directory: $PWD" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press any key to close..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Host "[DEBUG] ufa_pipeline_viewer.py found" -ForegroundColor DarkGray

# Determine which Python to use - MUST use external venv
Write-Host "[DEBUG] Determining Python executable..." -ForegroundColor DarkGray
$pythonCmd = "c:\Users\Cliff.Thelin\Source\ufa\ufa_venv\Scripts\python.exe"

if (Test-Path $pythonCmd) {
    Write-Host "[DEBUG] Using external venv Python: $pythonCmd" -ForegroundColor DarkGray
    Write-Host "[DEBUG] Virtual environment will be used" -ForegroundColor Green
} elseif (Test-Path "ufa_venv\Scripts\python.exe") {
    $pythonCmd = ".\ufa_venv\Scripts\python.exe"
    Write-Host "[DEBUG] Using local ufa_venv Python: $pythonCmd" -ForegroundColor Yellow
    Write-Host "[WARNING] Local ufa_venv may have incomplete packages" -ForegroundColor Yellow
} else {
    $pythonCmd = "python"
    Write-Host "[DEBUG] Using system Python" -ForegroundColor Red
    Write-Host "[WARNING] Virtual environment not found!" -ForegroundColor Red
}

# CRITICAL: Verify Python and packages one more time before launch
Write-Host "[DEBUG] Final precheck before launch..." -ForegroundColor DarkGray
$finalPython = & $pythonCmd -c "import sys; print(sys.executable)" 2>&1
Write-Host "[DEBUG] Python executable: $finalPython" -ForegroundColor DarkGray
Write-Host "[DEBUG] Testing GUI packages: customtkinter, pandas, tkinter" -ForegroundColor DarkGray

$finalTest = & $pythonCmd -c "import customtkinter, pandas, tkinter; print('READY')" 2>&1
if ($finalTest -notmatch "READY") {
    Write-Host ""
    Write-Host "="*60 -ForegroundColor Red
    Write-Host "CRITICAL ERROR: Packages not available!" -ForegroundColor Red
    Write-Host "="*60 -ForegroundColor Red
    Write-Host ""
    Write-Host "Python being used: $finalPython" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Import test failed with:" -ForegroundColor Yellow
    Write-Host $finalTest -ForegroundColor Gray
    Write-Host ""
    Write-Host "This should not happen! The precheck passed but imports are failing." -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible causes:" -ForegroundColor Yellow
    Write-Host "  1. Virtual environment activation didn't work" -ForegroundColor Gray
    Write-Host "  2. Wrong Python executable is being used" -ForegroundColor Gray
    Write-Host "  3. Packages installed in different Python" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Quick fix - Install packages now:" -ForegroundColor Cyan
    Write-Host "  python -m pip install customtkinter pandas pillow" -ForegroundColor Gray
    Write-Host ""
    
    if (Get-UserConfirmation "Try to install packages now?") {
        Write-Host ""
        Write-Host "Installing packages..." -ForegroundColor Cyan
        & $pythonCmd -m pip install --upgrade pip -q
        & $pythonCmd -m pip install customtkinter pandas pillow
        
        # Install pipeline packages if requirements.txt exists
        if (Test-Path "requirements.txt") {
            Write-Host "Installing pipeline packages from requirements.txt..." -ForegroundColor Gray
            & $pythonCmd -m pip install -r requirements.txt
        }
        
        # Test again
        $retestImport = & $pythonCmd -c "import customtkinter, pandas, tkinter; print('OK')" 2>&1
        if ($retestImport -match "OK") {
            Write-Host "✓ GUI packages installed successfully" -ForegroundColor Green
            Write-Host ""
        } else {
            Write-Host "✗ Installation failed" -ForegroundColor Red
            Write-Host $retestImport -ForegroundColor Gray
            Write-Host ""
            Write-Host "Press any key to exit..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    } else {
        Write-Host ""
        Write-Host "Cannot continue without packages." -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

Write-Host "[DEBUG] Final precheck PASSED - packages are available" -ForegroundColor DarkGray

# Launch application and wait for it to complete
Write-Host ""
Write-Host "[DEBUG] About to launch Python application..." -ForegroundColor DarkGray
Write-Host "Application window should open shortly..." -ForegroundColor Cyan
Write-Host "(This console will remain open until the application closes)" -ForegroundColor Gray
Write-Host ""
Write-Host "[DEBUG] Running: $pythonCmd ufa_pipeline_viewer.py" -ForegroundColor DarkGray
Write-Host "" -NoNewline  # Ensure flush

try {
    # Create a temporary file for error output
    $errorFile = Join-Path $env:TEMP "ufa_viewer_error.txt"
    
    # Run and capture both stdout and stderr
    & $pythonCmd ufa_pipeline_viewer.py 2>$errorFile
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor $(if ($exitCode -ne 0) { "Red" } else { "Green" })
    if ($exitCode -ne 0) {
        Write-Host "[X] APPLICATION ERROR" -ForegroundColor Red
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "Application exited with error code: $exitCode" -ForegroundColor Yellow
        Write-Host ""
        
        # Show error details if available
        if (Test-Path $errorFile) {
            $errorContent = Get-Content $errorFile -Raw
            if ($errorContent.Trim()) {
                Write-Host "Error details:" -ForegroundColor Yellow
                Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
                Write-Host $errorContent -ForegroundColor Gray
                Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor DarkGray
                Write-Host ""
            }
            Remove-Item $errorFile -ErrorAction SilentlyContinue
        }
        
        Write-Host "Common issues:" -ForegroundColor Yellow
        Write-Host "  • Missing packages: pip install customtkinter pandas pillow" -ForegroundColor Gray
        Write-Host "  • File path issue: Check final_output folder exists" -ForegroundColor Gray
        Write-Host "  • Import error: Verify email_formatter.py is present" -ForegroundColor Gray
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Red
        Write-Host "WINDOW WILL STAY OPEN - Review errors above" -ForegroundColor Yellow
        Write-Host "========================================" -ForegroundColor Red
    } else {
        Write-Host "[OK] APPLICATION CLOSED NORMALLY" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
    }
    Write-Host ""
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "[X] FAILED TO LAUNCH APPLICATION" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Error details:" -ForegroundColor Yellow
    Write-Host $_.Exception.Message -ForegroundColor Gray
    Write-Host ""
    Write-Host "Stack trace:" -ForegroundColor Yellow
    Write-Host $_.ScriptStackTrace -ForegroundColor Gray
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "WINDOW WILL STAY OPEN - Review errors above" -ForegroundColor Yellow
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
}

Write-Host "Press any key to close this window..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
