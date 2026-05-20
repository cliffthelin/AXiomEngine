# Pre-Commit Safety Check for UFA Pipeline
# Prevents accidental commit of sensitive data to GitHub

Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host "🔍 UFA Pipeline - Pre-Commit Safety Check" -ForegroundColor Cyan
Write-Host "=" * 80 -ForegroundColor Cyan
Write-Host ""

$issues = @()
$warnings = @()

# Get list of staged files
try {
    $stagedFiles = git diff --cached --name-only 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "⚠️  Not a git repository or git not available" -ForegroundColor Yellow
        exit 0
    }
} catch {
    Write-Host "⚠️  Unable to check git status" -ForegroundColor Yellow
    exit 0
}

if (-not $stagedFiles) {
    Write-Host "ℹ️  No files staged for commit" -ForegroundColor Gray
    exit 0
}

Write-Host "📋 Checking $($stagedFiles.Count) staged file(s)...`n" -ForegroundColor White

# Critical checks (BLOCK commit)
# ================================

# 1. Check for appsettings.json
if ($stagedFiles -match "appsettings\.json$") {
    $issues += "appsettings.json - Contains database credentials and server names"
}

# 2. Check for CSV files (contain PII)
$csvFiles = $stagedFiles | Where-Object { $_ -match "\.csv$" }
if ($csvFiles) {
    $issues += "$($csvFiles.Count) CSV file(s) - Contains student PII (names, emails, SSIDs)"
}

# 3. Check for Excel files (may contain PII)
$excelFiles = $stagedFiles | Where-Object { $_ -match "\.(xlsx|xlsm|xls)$" }
if ($excelFiles) {
    $issues += "$($excelFiles.Count) Excel file(s) - May contain sensitive source data"
}

# 4. Check for output directories
$outputFiles = $stagedFiles | Where-Object { 
    $_ -match "(final_output|created_file_references|ufa_files)/" 
}
if ($outputFiles) {
    $issues += "$($outputFiles.Count) output file(s) - Contains generated data with PII"
}

# 5. Check for pipeline state
if ($stagedFiles -match "pipeline_state\.json") {
    $issues += "pipeline_state.json - Contains runtime paths and state"
}

# 6. Check for user config
if ($stagedFiles -match "user_config\.toml$") {
    $issues += "user_config.toml - Contains environment-specific settings"
}

# 7. Check for log files
$logFiles = $stagedFiles | Where-Object { $_ -match "\.(log|bak|tmp)$" }
if ($logFiles) {
    $issues += "$($logFiles.Count) log/backup file(s) - May contain sensitive paths"
}

# Warning checks (WARN but allow)
# =================================

# 1. Check for executed notebooks
$executedNotebooks = $stagedFiles | Where-Object { $_ -match "_executed\.ipynb$" }
if ($executedNotebooks) {
    $warnings += "$($executedNotebooks.Count) executed notebook(s) - May contain output with PII"
}

# 2. Check for Python files with hardcoded database strings
$pythonFiles = $stagedFiles | Where-Object { $_ -match "\.py$" }
foreach ($file in $pythonFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
        if ($content -match "UTRX-DB-P-W4|Server=.*Database=") {
            $warnings += "$file - May contain hardcoded database connections"
        }
        if ($content -match "@(utah\.gov|utah\.edu|byui\.edu)") {
            $warnings += "$file - Contains email addresses"
        }
    }
}

# 3. Check Jupyter notebooks for hardcoded credentials
$notebookFiles = $stagedFiles | Where-Object { $_ -match "\.ipynb$" -and $_ -notmatch "_executed" }
foreach ($file in $notebookFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw -ErrorAction SilentlyContinue
        if ($content -match "UTRX-DB-P-W4") {
            $warnings += "$file - Contains hardcoded server name"
        }
        if ($content -match "C:\\\\Users\\\\Cliff\.Thelin") {
            $warnings += "$file - Contains user-specific paths"
        }
    }
}

# Display Results
# ===============

Write-Host "=" * 80 -ForegroundColor White

if ($issues.Count -eq 0 -and $warnings.Count -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED - Safe to commit!" -ForegroundColor Green
    Write-Host "=" * 80 -ForegroundColor White
    Write-Host ""
    exit 0
}

if ($issues.Count -gt 0) {
    Write-Host "🚨 COMMIT BLOCKED - Critical Security Issues Found" -ForegroundColor Red
    Write-Host "=" * 80 -ForegroundColor Red
    Write-Host ""
    Write-Host "The following files contain sensitive data and MUST NOT be committed:" -ForegroundColor Yellow
    Write-Host ""
    foreach ($issue in $issues) {
        Write-Host "  ❌ $issue" -ForegroundColor Red
    }
    Write-Host ""
    Write-Host "Fix these issues before committing:" -ForegroundColor Yellow
    Write-Host "  1. Unstage sensitive files: git reset HEAD <file>" -ForegroundColor White
    Write-Host "  2. Verify .gitignore is configured: cat .gitignore" -ForegroundColor White
    Write-Host "  3. Add files to .gitignore if needed" -ForegroundColor White
    Write-Host ""
}

if ($warnings.Count -gt 0) {
    if ($issues.Count -eq 0) {
        Write-Host "⚠️  WARNINGS DETECTED - Review Before Committing" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️  ADDITIONAL WARNINGS" -ForegroundColor Yellow
    }
    Write-Host "=" * 80 -ForegroundColor Yellow
    Write-Host ""
    Write-Host "The following files may need review:" -ForegroundColor Yellow
    Write-Host ""
    foreach ($warning in $warnings) {
        Write-Host "  ⚠️  $warning" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "Recommended actions:" -ForegroundColor Yellow
    Write-Host "  • Review files for hardcoded credentials or PII" -ForegroundColor White
    Write-Host "  • Clear notebook output before committing" -ForegroundColor White
    Write-Host "  • Verify no sensitive data in output cells" -ForegroundColor White
    Write-Host ""
}

Write-Host "=" * 80 -ForegroundColor White
Write-Host ""

if ($issues.Count -gt 0) {
    Write-Host "📖 For more information, see: GITHUB_SAFETY_GUIDE.md" -ForegroundColor Cyan
    Write-Host ""
    exit 1  # Block commit
} else {
    Write-Host "⚠️  Warnings found but allowing commit. Please review carefully." -ForegroundColor Yellow
    Write-Host "📖 For more information, see: GITHUB_SAFETY_GUIDE.md" -ForegroundColor Cyan
    Write-Host ""
    exit 0  # Allow commit with warnings
}
