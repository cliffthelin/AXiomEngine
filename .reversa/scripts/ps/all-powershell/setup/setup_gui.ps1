# UFA Student History Viewer - Quick Setup
# This script installs dependencies and launches the application

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   UFA Student History Viewer Setup   " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found!" -ForegroundColor Red
    Write-Host "  Please install Python 3.9+ from python.org" -ForegroundColor Red
    pause
    exit 1
}

# Check if we're in virtual environment
Write-Host ""
Write-Host "Checking for virtual environment..." -ForegroundColor Yellow
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Using virtual environment: $env:VIRTUAL_ENV" -ForegroundColor Green
} else {
    Write-Host "⚠ Not in virtual environment" -ForegroundColor Yellow
    Write-Host "  Recommended: activate ufa_venv first" -ForegroundColor Yellow
    
    $response = Read-Host "Continue anyway? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Setup cancelled." -ForegroundColor Gray
        pause
        exit 0
    }
}

# Install dependencies
Write-Host ""
Write-Host "Installing GUI dependencies..." -ForegroundColor Yellow
Write-Host "  - customtkinter (modern UI framework)" -ForegroundColor Gray
Write-Host "  - pandas (data processing)" -ForegroundColor Gray
Write-Host "  - pillow (image support)" -ForegroundColor Gray
Write-Host ""

try {
    python -m pip install --upgrade pip | Out-Null
    python -m pip install -r requirements_gui.txt
    
    Write-Host ""
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "  Try manually: pip install customtkinter pandas pillow" -ForegroundColor Red
    pause
    exit 1
}

# Check for data files
Write-Host ""
Write-Host "Checking for data files..." -ForegroundColor Yellow

$historyFile = "final_output\change_history\student_change_history.csv"
$reportFiles = Get-ChildItem "final_output\Cross-Enrolled-*.csv" -ErrorAction SilentlyContinue

if (Test-Path $historyFile) {
    $historyLines = (Get-Content $historyFile).Count - 1
    Write-Host "✓ Found history file: $historyLines records" -ForegroundColor Green
} else {
    Write-Host "⚠ No history file found" -ForegroundColor Yellow
    Write-Host "  Run the pipeline at least twice to build history" -ForegroundColor Yellow
}

if ($reportFiles) {
    $latestReport = $reportFiles | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    Write-Host "✓ Found report: $($latestReport.Name)" -ForegroundColor Green
} else {
    Write-Host "⚠ No report files found" -ForegroundColor Yellow
    Write-Host "  Run the pipeline to generate reports" -ForegroundColor Yellow
}

# Launch application
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!                    " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Launch the application now? (y/n)" -ForegroundColor Yellow
$launch = Read-Host

if ($launch -eq 'y') {
    Write-Host ""
    Write-Host "Launching Student History Viewer..." -ForegroundColor Green
    Write-Host ""
    python student_history_gui.py
} else {
    Write-Host ""
    Write-Host "To launch manually, run:" -ForegroundColor Cyan
    Write-Host "  python student_history_gui.py" -ForegroundColor White
    Write-Host ""
    pause
}
