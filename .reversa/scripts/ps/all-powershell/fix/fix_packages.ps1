# Fix Package Installation
# Run this if launcher says packages are installed but app still fails

Write-Host "=" * 60
Write-Host "UFA Pipeline Viewer - Package Fix Utility"
Write-Host "=" * 60
Write-Host ""

# Show which Python is active
$pythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
$pythonVersion = python --version 2>&1

Write-Host "Current Python:" -ForegroundColor Cyan
Write-Host "  Executable: $pythonExe" -ForegroundColor White
Write-Host "  Version: $pythonVersion" -ForegroundColor White
Write-Host ""

# Check if venv exists
if (Test-Path "ufa_venv") {
    Write-Host "Virtual environment found: ufa_venv" -ForegroundColor Green
    Write-Host "Activating..." -ForegroundColor Yellow
    & .\ufa_venv\Scripts\Activate.ps1 2>$null
    
    $venvPython = (Get-Command python -ErrorAction SilentlyContinue).Source
    Write-Host "  Venv Python: $venvPython" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "No virtual environment found" -ForegroundColor Yellow
    Write-Host "Installing to system Python..." -ForegroundColor Yellow
    Write-Host ""
}

# Test current package status
Write-Host "Testing package imports..." -ForegroundColor Cyan
$packages = @("customtkinter", "pandas", "PIL", "numpy", "rapidfuzz", "openpyxl", "sklearn", "tensorflow", "joblib", "matplotlib", "seaborn", "xlsxwriter", "pyodbc", "tkinter")
$missing = @()

foreach ($pkg in $packages) {
    $test = python -c "import $pkg; print('OK')" 2>&1
    if ($test -match "OK") {
        Write-Host "  ✓ $pkg" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $pkg - MISSING" -ForegroundColor Red
        $missing += $pkg
    }
}

Write-Host ""

if ($missing.Count -eq 0) {
    Write-Host "✓ All packages are installed!" -ForegroundColor Green
    Write-Host ""
    Write-Host "The issue might be:" -ForegroundColor Yellow
    Write-Host "  • Different Python being used when launching" -ForegroundColor Gray
    Write-Host "  • Virtual environment not activating properly" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Try running the app directly:" -ForegroundColor Cyan
    Write-Host "  python ufa_pipeline_viewer.py" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "Missing packages detected: $($missing -join ', ')" -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing now..." -ForegroundColor Cyan
    Write-Host ""
    
    # Install with verbose output
    python -m pip install --upgrade pip
    Write-Host ""
    Write-Host "Installing GUI packages..." -ForegroundColor Cyan
    python -m pip install customtkinter pandas pillow
    
    # Install pipeline packages if requirements.txt exists
    if (Test-Path "requirements.txt") {
        Write-Host ""
        Write-Host "Installing pipeline packages from requirements.txt..." -ForegroundColor Cyan
        python -m pip install -r requirements.txt
    }
    
    Write-Host ""
    Write-Host "Verifying installation..." -ForegroundColor Cyan
    
    # Test again
    $allOk = $true
    foreach ($pkg in $packages) {
        $test = python -c "import $pkg; print('OK')" 2>&1
        if ($test -match "OK") {
            Write-Host "  ✓ $pkg" -ForegroundColor Green
        } else {
            Write-Host "  ✗ $pkg - STILL MISSING" -ForegroundColor Red
            $allOk = $false
        }
    }
    
    Write-Host ""
    if ($allOk) {
        Write-Host "✓ Installation successful!" -ForegroundColor Green
        Write-Host ""
        Write-Host "You can now run:" -ForegroundColor Cyan
        Write-Host "  .\launch_gui.ps1" -ForegroundColor White
        Write-Host "  or" -ForegroundColor Gray
        Write-Host "  python ufa_pipeline_viewer.py" -ForegroundColor White
    } else {
        Write-Host "✗ Installation failed" -ForegroundColor Red
        Write-Host ""
        Write-Host "Try manually:" -ForegroundColor Yellow
        Write-Host "  python -m pip install --upgrade pip" -ForegroundColor Gray
        Write-Host "  python -m pip install customtkinter pandas pillow" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "=" * 60
Write-Host ""
pause
