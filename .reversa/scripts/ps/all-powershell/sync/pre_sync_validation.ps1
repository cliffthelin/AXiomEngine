# Pre-Sync Safety Validation Script
# REQUIRED before any data synchronization between systems

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('git', 'database', 'file_transfer', 'model_deployment', 'all')]
    [string]$SyncType = 'all',
    
    [Parameter(Mandatory=$false)]
    [switch]$BlockOnWarnings = $false
)

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "      PRE-SYNC SAFETY VALIDATION - Multi-System Data Transfer" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorCount = 0
$WarningCount = 0
$ValidationPassed = $true

# =============================================================================
# 1. GIT SYNC VALIDATION
# =============================================================================

if ($SyncType -in @('git', 'all')) {
    Write-Host "=== GIT SYNC VALIDATION ===" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if in git repository
    $isGitRepo = Test-Path ".git"
    
    if ($isGitRepo) {
        # Check for staged sensitive files
        $stagedFiles = git diff --cached --name-only 2>$null
        $sensitiveStagedFiles = $stagedFiles | Where-Object { 
            $_ -match "\.(csv|xlsx|xlsm|keras|pkl|h5)$" -or 
            $_ -match "appsettings\.json$" -or
            $_ -match "training|exclusion|student_history|pipeline_state" 
        }
        
        if ($sensitiveStagedFiles) {
            Write-Host "  ❌ BLOCKED: Sensitive files in staging area:" -ForegroundColor Red
            foreach ($file in $sensitiveStagedFiles) {
                Write-Host "     - $file" -ForegroundColor Red
            }
            $ErrorCount++
            $ValidationPassed = $false
        } else {
            Write-Host "  ✅ No sensitive files staged for commit" -ForegroundColor Green
        }
        
        # Check for uncommitted changes to critical files
        $modifiedFiles = git diff --name-only 2>$null
        $criticalModified = $modifiedFiles | Where-Object { 
            $_ -match "config|settings|schema" -and $_ -match "\.(py|json|md)$"
        }
        
        if ($criticalModified) {
            Write-Host "  ⚠️  WARNING: Uncommitted changes to configuration files:" -ForegroundColor Yellow
            foreach ($file in $criticalModified) {
                Write-Host "     - $file" -ForegroundColor Yellow
            }
            $WarningCount++
            if ($BlockOnWarnings) { $ValidationPassed = $false }
        }
    } else {
        Write-Host "  ℹ️  Not a git repository - skipping git checks" -ForegroundColor Cyan
    }
    Write-Host ""
}

# =============================================================================
# 2. FILE TRANSFER VALIDATION
# =============================================================================

if ($SyncType -in @('file_transfer', 'all')) {
    Write-Host "=== FILE TRANSFER VALIDATION ===" -ForegroundColor Yellow
    Write-Host ""
    
    # Check for data files that should never leave local system
    $localOnlyPatterns = @(
        "final_ml_training*.csv",
        "UFA_Exclusion*.xlsx",
        "student_history*.csv",
        "appsettings.json",
        "*.keras",
        "*.pkl"
    )
    
    $foundLocalOnlyFiles = @()
    foreach ($pattern in $localOnlyPatterns) {
        $matches = Get-ChildItem -Path . -Filter $pattern -Recurse -File -ErrorAction SilentlyContinue
        if ($matches) {
            $foundLocalOnlyFiles += $matches
        }
    }
    
    if ($foundLocalOnlyFiles.Count -gt 0) {
        Write-Host "  ⚠️  WARNING: Found $($foundLocalOnlyFiles.Count) files that should NEVER be transferred:" -ForegroundColor Yellow
        foreach ($file in $foundLocalOnlyFiles | Select-Object -First 5) {
            Write-Host "     - $($file.FullName)" -ForegroundColor Yellow
        }
        if ($foundLocalOnlyFiles.Count -gt 5) {
            Write-Host "     ... and $($foundLocalOnlyFiles.Count - 5) more" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "  ⚠️  These files contain PII and must remain on local system only" -ForegroundColor Yellow
        $WarningCount += $foundLocalOnlyFiles.Count
    } else {
        Write-Host "  ✅ No local-only files found in current directory" -ForegroundColor Green
    }
    Write-Host ""
}

# =============================================================================
# 3. DATABASE SYNC VALIDATION
# =============================================================================

if ($SyncType -in @('database', 'all')) {
    Write-Host "=== DATABASE SYNC VALIDATION ===" -ForegroundColor Yellow
    Write-Host ""
    
    # Check if appsettings.json exists and has valid structure
    if (Test-Path "appsettings.json") {
        try {
            $appSettings = Get-Content "appsettings.json" -Raw | ConvertFrom-Json
            
            # Check for placeholder credentials (should fail if using defaults)
            if ($appSettings.ConnectionStrings) {
                foreach ($connName in $appSettings.ConnectionStrings.PSObject.Properties.Name) {
                    $connString = $appSettings.ConnectionStrings.$connName
                    if ($connString -match "YOUR_|PLACEHOLDER|CHANGEME|password=;|password=$") {
                        Write-Host "  ❌ BLOCKED: Database connection using placeholder credentials: $connName" -ForegroundColor Red
                        $ErrorCount++
                        $ValidationPassed = $false
                    }
                }
            }
            
            Write-Host "  ✅ Database configuration appears valid" -ForegroundColor Green
            
        } catch {
            Write-Host "  ⚠️  WARNING: Could not parse appsettings.json" -ForegroundColor Yellow
            $WarningCount++
        }
    } else {
        Write-Host "  ℹ️  No appsettings.json found - skipping DB validation" -ForegroundColor Cyan
    }
    Write-Host ""
}

# =============================================================================
# 4. ML MODEL DEPLOYMENT VALIDATION
# =============================================================================

if ($SyncType -in @('model_deployment', 'all')) {
    Write-Host "=== ML MODEL DEPLOYMENT VALIDATION ===" -ForegroundColor Yellow
    Write-Host ""
    
    # Check for model files
    $modelFiles = Get-ChildItem -Path . -Include "*.keras","*.pkl","*.h5","*.joblib" -Recurse -File -ErrorAction SilentlyContinue
    
    if ($modelFiles) {
        Write-Host "  ⚠️  WARNING: Found $($modelFiles.Count) ML model file(s):" -ForegroundColor Yellow
        foreach ($model in $modelFiles | Select-Object -First 3) {
            Write-Host "     - $($model.Name)" -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "  ⚠️  ML models contain PII patterns and should NOT be deployed to shared systems" -ForegroundColor Yellow
        Write-Host "  ⚠️  Models should be retrained in target environment using local data only" -ForegroundColor Yellow
        $WarningCount += $modelFiles.Count
        
        if ($BlockOnWarnings) { 
            $ValidationPassed = $false 
            $ErrorCount++
        }
    } else {
        Write-Host "  ✅ No ML model files found" -ForegroundColor Green
    }
    Write-Host ""
}

# =============================================================================
# 5. PII DATA VALIDATION
# =============================================================================

Write-Host "=== PII DATA VALIDATION ===" -ForegroundColor Yellow
Write-Host ""

# Check for files with potential PII
$piiPatterns = @(
    "*.csv",
    "*.xlsx", 
    "*.xlsm"
)

$piiFiles = @()
foreach ($pattern in $piiPatterns) {
    $matches = Get-ChildItem -Path . -Filter $pattern -File -ErrorAction SilentlyContinue
    if ($matches) {
        $piiFiles += $matches
    }
}

if ($piiFiles.Count -gt 0) {
    Write-Host "  ⚠️  WARNING: Found $($piiFiles.Count) file(s) that may contain PII:" -ForegroundColor Yellow
    foreach ($file in $piiFiles | Select-Object -First 5) {
        $size = [math]::Round($file.Length / 1KB, 2)
        Write-Host "     - $($file.Name) ($size KB)" -ForegroundColor Yellow
    }
    if ($piiFiles.Count -gt 5) {
        Write-Host "     ... and $($piiFiles.Count - 5) more" -ForegroundColor Yellow
    }
    Write-Host ""
    Write-Host "  ⚠️  Verify these files do NOT contain student data before syncing" -ForegroundColor Yellow
    $WarningCount += $piiFiles.Count
} else {
    Write-Host "  ✅ No CSV/Excel files found in current directory" -ForegroundColor Green
}
Write-Host ""

# =============================================================================
# 6. PIPELINE STATE VALIDATION
# =============================================================================

Write-Host "=== PIPELINE STATE VALIDATION ===" -ForegroundColor Yellow
Write-Host ""

if (Test-Path "pipeline_state.json") {
    try {
        $pipelineState = Get-Content "pipeline_state.json" -Raw | ConvertFrom-Json
        Write-Host "  ✅ Pipeline state file exists and is valid JSON" -ForegroundColor Green
        
        # Check for file paths in state (might contain local paths)
        if ($pipelineState.PSObject.Properties.Name -match "path|file|directory") {
            Write-Host "  ℹ️  Pipeline state contains file paths - verify compatibility with target system" -ForegroundColor Cyan
        }
    } catch {
        Write-Host "  ⚠️  WARNING: Pipeline state file exists but is not valid JSON" -ForegroundColor Yellow
        $WarningCount++
    }
} else {
    Write-Host "  ℹ️  No pipeline state file found" -ForegroundColor Cyan
}
Write-Host ""

# =============================================================================
# 7. CONFIGURATION VALIDATION
# =============================================================================

Write-Host "=== CONFIGURATION VALIDATION ===" -ForegroundColor Yellow
Write-Host ""

# Check for configuration files
$configFiles = @(
    "appsettings.json",
    "config.py",
    "config_manager.py",
    "launcher_config.json"
)

foreach ($configFile in $configFiles) {
    if (Test-Path $configFile) {
        $content = Get-Content $configFile -Raw
        
        # Check for hardcoded credentials or PII
        $suspiciousPatterns = @(
            "password\s*=\s*['\`"][^'\`"]{3,}",
            "api[_-]?key\s*=\s*['\`"][^'\`"]{10,}",
            "secret\s*=\s*['\`"][^'\`"]{10,}",
            "token\s*=\s*['\`"][^'\`"]{10,}"
        )
        
        $foundSuspicious = $false
        foreach ($pattern in $suspiciousPatterns) {
            if ($content -match $pattern) {
                if (-not $foundSuspicious) {
                    Write-Host "  ⚠️  WARNING: $configFile may contain hardcoded credentials" -ForegroundColor Yellow
                    $WarningCount++
                    $foundSuspicious = $true
                }
            }
        }
        
        if (-not $foundSuspicious) {
            Write-Host "  ✅ $configFile appears safe" -ForegroundColor Green
        }
    }
}
Write-Host ""

# =============================================================================
# SUMMARY AND DECISION
# =============================================================================

Write-Host "=====================================================================" -ForegroundColor Cyan
Write-Host "VALIDATION SUMMARY" -ForegroundColor Cyan
Write-Host "=====================================================================" -ForegroundColor Cyan

Write-Host "Sync Type: $SyncType" -ForegroundColor Cyan
Write-Host "Errors: $ErrorCount" -ForegroundColor $(if ($ErrorCount -gt 0) { "Red" } else { "Green" })
Write-Host "Warnings: $WarningCount" -ForegroundColor $(if ($WarningCount -gt 0) { "Yellow" } else { "Green" })
Write-Host ""

if ($ErrorCount -gt 0) {
    Write-Host "❌ SYNC BLOCKED - CRITICAL ISSUES FOUND" -ForegroundColor Red
    Write-Host ""
    Write-Host "You MUST resolve the errors above before syncing data." -ForegroundColor Red
    Write-Host "These errors indicate PII or sensitive data that should never leave this system." -ForegroundColor Red
    exit 1
} elseif ($WarningCount -gt 0) {
    if ($BlockOnWarnings) {
        Write-Host "⚠️  SYNC BLOCKED - WARNINGS FOUND (BlockOnWarnings enabled)" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Review all warnings above before proceeding." -ForegroundColor Yellow
        Write-Host "Use -BlockOnWarnings:`$false to allow sync with warnings." -ForegroundColor Yellow
        exit 1
    } else {
        Write-Host "⚠️  $WarningCount WARNING(S) FOUND - REVIEW REQUIRED" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Warnings indicate potential issues but sync is allowed." -ForegroundColor Yellow
        Write-Host "Review warnings carefully before proceeding with sync." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "Sync can proceed - but verify data safety first! ⚠️" -ForegroundColor Yellow
        exit 0
    }
} else {
    Write-Host "✅ ALL VALIDATIONS PASSED" -ForegroundColor Green
    Write-Host ""
    Write-Host "Safe to proceed with sync! ✓" -ForegroundColor Green
    exit 0
}
