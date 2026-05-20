# Update all processing notebooks to use ufa_venv kernel
$notebooks = @(
    "05_Process_Identity.ipynb",
    "06_Process_Enrollment.ipynb",
    "07_Process_Eligibility.ipynb",
    "08_Process_Exclusions.ipynb",
    "09_Final_Reporting.ipynb",
    "01_Train_Data_Builder.ipynb",
    "02_Train_Identity_Model.ipynb",
    "03_Train_Eligibility.ipynb",
    "04_Train_Model_Validation.ipynb"
)

Write-Host "Updating kernel metadata for notebooks..." -ForegroundColor Cyan

foreach ($notebook in $notebooks) {
    if (Test-Path $notebook) {
        Write-Host "  Processing: $notebook" -ForegroundColor Yellow
        
        # Read the JSON
        $content = Get-Content $notebook -Raw | ConvertFrom-Json
        
        # Update kernelspec
        $content.metadata.kernelspec = @{
            "display_name" = "Python (ufa_venv)"
            "language" = "python"
            "name" = "ufa_venv"
        }
        
        # Save back
        $content | ConvertTo-Json -Depth 100 | Set-Content $notebook -Encoding UTF8
        
        Write-Host "    ✅ Updated" -ForegroundColor Green
    } else {
        Write-Host "    ⚠️  Not found: $notebook" -ForegroundColor Red
    }
}

Write-Host "`n✅ All notebooks updated to use ufa_venv kernel" -ForegroundColor Green
Write-Host "   Kernel: Python (ufa_venv)" -ForegroundColor Cyan
Write-Host "   Location: C:\Users\Cliff.Thelin\AppData\Roaming\jupyter\kernels\ufa_venv" -ForegroundColor Cyan
