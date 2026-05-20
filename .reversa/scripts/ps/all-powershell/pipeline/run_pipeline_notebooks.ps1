# Run pipeline notebooks and check results
Write-Host "=== Running Pipeline Notebooks ===" -ForegroundColor Cyan

# NB05 - Already completed
Write-Host "`n[1/3] NB05 Identity Processing - ALREADY COMPLETED" -ForegroundColor Green

# NB06 - Already completed  
Write-Host "[2/3] NB06 Enrollment Processing - ALREADY COMPLETED" -ForegroundColor Green

# NB07 - Eligibility
Write-Host "`n[3/3] Running NB07 Eligibility..." -ForegroundColor Yellow
C:\Users\Cliff.Thelin\Source\ufa26\ufa_venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 "07_Process_Eligibility.ipynb" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ NB07 completed successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ NB07 failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

# NB08 - Exclusions
Write-Host "`nRunning NB08 Exclusions..." -ForegroundColor Yellow
C:\Users\Cliff.Thelin\Source\ufa26\ufa_venv\Scripts\python.exe -m jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=600 "08_Process_Exclusions.ipynb" 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ NB08 completed successfully" -ForegroundColor Green
} else {
    Write-Host "  ✗ NB08 failed with exit code $LASTEXITCODE" -ForegroundColor Red
    exit 1
}

# Check final results
Write-Host "`n=== Checking New Columns ===" -ForegroundColor Cyan
python check_new_columns.py

Write-Host "`n=== Pipeline Complete ===" -ForegroundColor Green
