$logPath = "c:\Users\Cliff.Thelin\Source\ufa26\ufa_new_data\run_logs\python_config_diagnostic.log"
Write-Host "=== MONITORING RUN 7 ===" -ForegroundColor Cyan
Write-Host "Started: $(Get-Date -Format 'HH:mm:ss')`n"

for ($i = 1; $i -le 25; $i++) {
    Write-Host "[$i/25] $(Get-Date -Format 'HH:mm:ss')  " -NoNewline -ForegroundColor Yellow
    
    if (Test-Path $logPath) {
        $content = Get-Content $logPath -Raw
        $lineCount = ($content -split "`n").Count
        Write-Host "$lineCount lines"
        
        # Check for errors
        if ($content -match "❌|FAILED|RuntimeError") {
            Write-Host "`nERROR DETECTED!" -ForegroundColor Red
            ($content -split "`n") | Select-Object -Last 30
            break
        }
        
        # Check for completion
        if ($content -match "All reporting notebooks completed") {
            Write-Host "`nPIPELINE COMPLETE!" -ForegroundColor Green
            ($content -split "`n") | Select-Object -Last 40
            break
        }
    }
    
    if ($i -lt 25) {
        Start-Sleep -Seconds 150  # 2.5 minutes
    }
}

Write-Host "`n=== END MONITORING ===" -ForegroundColor Cyan
