# Quick fix: Rename files with malformed date 03-204-2026 to correct date 03-04-2026
$oldDate = "03-204-2026"
$newDate = "03-04-2026"
$directory = "created_file_references"

Write-Host "Renaming files with date $oldDate to $newDate..." -ForegroundColor Cyan

$files = Get-ChildItem -Path $directory -Filter "*$oldDate*"

if ($files.Count -eq 0) {
    Write-Host "No files found with date $oldDate" -ForegroundColor Yellow
} else {
    foreach ($file in $files) {
        $newName = $file.Name -replace [regex]::Escape($oldDate), $newDate
        $newPath = Join-Path $directory $newName
        
        if (Test-Path $newPath) {
            Write-Host "  ⚠️  Skipping (already exists): $newName" -ForegroundColor Yellow
        } else {
            Rename-Item -Path $file.FullName -NewName $newName
            Write-Host "  ✅ Renamed: $($file.Name) → $newName" -ForegroundColor Green
        }
    }
    
    Write-Host "`n✅ Files renamed successfully!" -ForegroundColor Green
    Write-Host "   You can now run the processing notebooks" -ForegroundColor Cyan
}
