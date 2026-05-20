# Git Safety Check - Training Data Protection
# This script verifies no training data or PII will be committed to GitHub

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "      GIT SAFETY CHECK - Training Data Protection" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0

# =============================================================================
# 1. Check for staged files that should NEVER be committed
# =============================================================================

Write-Host "Checking for dangerous files in staging area..." -ForegroundColor Yellow

$DangerousPatterns = @(
    # Training data
    "*.csv",
    "**/ufa_training_data/*",
    "final_ml_training*.csv",
    "false_positives_for_training.csv",
    "*_BACKUP_*.csv",
    
    # PII files
    "*.xlsx",
    "*.xlsm",
    "UFA_Exclusion*.xlsx",
    "student_history*.csv",
    
    # Models and cache
    "*.keras",
    "*.pkl",
    "ml_models/*",
    "cache_*.pkl",
    "cache_*_metadata.json",
    
    # Configuration with credentials
    "appsettings.json",
    "user_config.toml",
    
    # State and output
    "pipeline_state.json",
    "created_file_references/*",
    "final_output/*",
    "ufa_files/*",
    "change_history/*",
    
    # Logs
    "*.log",
    "run_logs/*"
)

$StagedFiles = git diff --cached --name-only 2>$null

if ($LASTEXITCODE -eq 0 -and $StagedFiles) {
    foreach ($pattern in $DangerousPatterns) {
        $matches = $StagedFiles | Where-Object { $_ -like $pattern }
        if ($matches) {
            foreach ($file in $matches) {
                Write-Host "  ❌ BLOCKED: $file" -ForegroundColor Red
                Write-Host "     This file contains PII or training data and MUST NOT be committed" -ForegroundColor Red
                $ErrorCount++
            }
        }
    }
}

# =============================================================================
# 2. Check .gitignore exists and has required patterns
# =============================================================================

Write-Host ""
Write-Host "Verifying .gitignore protection..." -ForegroundColor Yellow

$RequiredPatterns = @{
    "*.csv" = "CSV files (contain PII)"
    "*.xlsx" = "Excel files (contain PII)"
    "**/ufa_training_data/" = "Training data directory"
    "ml_models/" = "ML models directory"
    "*.keras" = "Keras model files"
    "*.pkl" = "Pickle cache files"
    "appsettings.json" = "Configuration with credentials"
    "UFA_Exclusion*.xlsx" = "Exclusion lists"
    "pipeline_state.json" = "Pipeline state"
    "final_output/" = "Output directory"
    "ufa_files/" = "Input files directory"
}

if (Test-Path ".gitignore") {
    $gitignoreContent = Get-Content ".gitignore" -Raw
    
    foreach ($pattern in $RequiredPatterns.Keys) {
        $description = $RequiredPatterns[$pattern]
        
        if ($gitignoreContent -match [regex]::Escape($pattern)) {
            Write-Host "  ✅ Protected: $pattern ($description)" -ForegroundColor Green
        } else {
            Write-Host "  ⚠️  MISSING: $pattern ($description)" -ForegroundColor Yellow
            $WarningCount++
        }
    }
    
    # Check for dangerous force-includes (ignore comments)
    $forceIncludes = $gitignoreContent -split "`n" | Where-Object { 
        $_ -match "^[^#]*!" -and ($_ -match "\.csv" -or $_ -match "training") 
    }
    if ($forceIncludes) {
        Write-Host "  ❌ DANGEROUS: .gitignore contains force-include (!) for sensitive files:" -ForegroundColor Red
        foreach ($line in $forceIncludes) {
            Write-Host "     $($line.Trim())" -ForegroundColor Red
        }
        $ErrorCount++
    }
    
} else {
    Write-Host "  ❌ ERROR: .gitignore file not found!" -ForegroundColor Red
    $ErrorCount++
}

# =============================================================================
# 3. Check if any tracked files match dangerous patterns
# =============================================================================

Write-Host ""
Write-Host "Scanning repository for tracked sensitive files..." -ForegroundColor Yellow

$TrackedFiles = git ls-files 2>$null

if ($LASTEXITCODE -eq 0 -and $TrackedFiles) {
    $DangerousTracked = @()
    
    foreach ($pattern in $DangerousPatterns) {
        $matches = $TrackedFiles | Where-Object { $_ -like $pattern }
        if ($matches) {
            $DangerousTracked += $matches
        }
    }
    
    if ($DangerousTracked.Count -gt 0) {
        Write-Host "  ⚠️  WARNING: Found $($DangerousTracked.Count) potentially sensitive file(s) already tracked:" -ForegroundColor Yellow
        foreach ($file in $DangerousTracked | Select-Object -First 10) {
            Write-Host "     - $file" -ForegroundColor Yellow
        }
        if ($DangerousTracked.Count -gt 10) {
            Write-Host "     ... and $($DangerousTracked.Count - 10) more" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "  ⚠️  To remove from tracking (but keep locally):" -ForegroundColor Yellow
        Write-Host "     git rm --cached <filename>" -ForegroundColor White
        $WarningCount += $DangerousTracked.Count
    } else {
        Write-Host "  ✅ No sensitive files currently tracked" -ForegroundColor Green
    }
}

# =============================================================================
# 4. Check remote URL (warn if public)
# =============================================================================

Write-Host ""
Write-Host "Checking repository configuration..." -ForegroundColor Yellow

$RemoteUrl = git config --get remote.origin.url 2>$null

if ($RemoteUrl) {
    Write-Host "  Repository URL: $RemoteUrl" -ForegroundColor Cyan
    
    if ($RemoteUrl -match "github\.com") {
        Write-Host "  ⚠️  WARNING: This is a GitHub repository" -ForegroundColor Yellow
        Write-Host "  ⚠️  Ensure it is private and NEVER make it public" -ForegroundColor Yellow
        Write-Host "  ⚠️  Training data and PII must stay local only" -ForegroundColor Yellow
        $WarningCount++
    }
}

# =============================================================================
# SUMMARY
# =============================================================================

Write-Host ""
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "SAFETY CHECK SUMMARY" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

if ($ErrorCount -eq 0 -and $WarningCount -eq 0) {
    Write-Host "✅ ALL CHECKS PASSED" -ForegroundColor Green
    Write-Host "   No dangerous files detected in staging area" -ForegroundColor Green
    Write-Host "   .gitignore properly configured" -ForegroundColor Green
    Write-Host ""
    Write-Host "Safe to commit! ✓" -ForegroundColor Green
    exit 0
} elseif ($ErrorCount -gt 0) {
    Write-Host "❌ COMMIT BLOCKED - $ErrorCount ERROR(S) FOUND" -ForegroundColor Red
    Write-Host ""
    Write-Host "CRITICAL: You are attempting to commit sensitive data!" -ForegroundColor Red
    Write-Host "Remove these files from staging before committing:" -ForegroundColor Red
    Write-Host "   git reset HEAD <filename>" -ForegroundColor White
    Write-Host ""
    Write-Host "These files contain PII and must NEVER be committed to any repository." -ForegroundColor Red
    exit 1
} else {
    Write-Host "⚠️  $WarningCount WARNING(S) FOUND" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Review warnings above before proceeding." -ForegroundColor Yellow
    Write-Host "Consider removing tracked sensitive files with:" -ForegroundColor Yellow
    Write-Host "   git rm --cached <filename>" -ForegroundColor White
    exit 0
}
