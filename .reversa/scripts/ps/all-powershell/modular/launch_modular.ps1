# UFA Pipeline Viewer Launcher - Modular Version
# This runs the new modular version

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  UFA USBE CROSS ENROLLMENT (Modular Version)" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting application..." -ForegroundColor Yellow
Write-Host ""

python main_ufa_viewer.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Application failed to start" -ForegroundColor Red
    Write-Host "Error code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Possible solutions:" -ForegroundColor Yellow
    Write-Host "  1. Check that Python is installed"
    Write-Host "  2. Run: pip install customtkinter pandas pillow tkcalendar"
    Write-Host "  3. Check that email_formatter.py exists"
    Write-Host ""
    Pause
}
