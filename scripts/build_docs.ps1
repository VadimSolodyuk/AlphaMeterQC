# AlphaMeterQC documentation build script for Windows PowerShell
# Обычная сборка (спросит про открытие браузера)
# .\scripts\build_docs.ps1

# Режим разработки с автооткрытием браузера
# .\scripts\build_docs.ps1 -Serve

# Режим разработки на порту 9000 с автооткрытием
# .\scripts\build_docs.ps1 -Serve -Port 9000

# Режим разработки БЕЗ автооткрытия браузера
# .\scripts\build_docs.ps1 -Serve -NoBrowser


# Configure UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

param(
    [switch]$Serve,
    [int]$Port = 8000,
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  MkDocs Documentation Build" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check virtual environment
$venvActivate = "venv\Scripts\Activate.ps1"
if (-not (Test-Path $venvActivate)) {
    Write-Host "[ERROR] Virtual environment not found." -ForegroundColor Red
    Write-Host "Run scripts\setup.ps1" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Gray
& $venvActivate

# Check MkDocs
try {
    $null = python -m mkdocs --version 2>&1
}
catch {
    Write-Host "[ERROR] MkDocs not installed." -ForegroundColor Red
    Write-Host "Run: pip install -e .[dev]" -ForegroundColor Red
    exit 1
}

if ($Serve) {
    # Development mode with auto-reload
    Write-Host "[INFO] Starting dev server on port $Port..." -ForegroundColor Gray
    Write-Host "Server URL: http://localhost:$Port" -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
    Write-Host ""

    # Open browser automatically (unless -NoBrowser is specified)
    if (-not $NoBrowser) {
        Write-Host "[INFO] Opening browser..." -ForegroundColor Gray
        # Используем cmd для открытия URL (надёжнее чем Start-Process)
        & "cmd" /c "start http://localhost:$Port"
        Start-Sleep -Seconds 2
    }

    # Start MkDocs dev server (blocks until Ctrl+C)
    python -m mkdocs serve --dev-addr "127.0.0.1:$Port"
}
else {
    # Build mode
    Write-Host "[INFO] Building documentation..." -ForegroundColor Gray
    Write-Host ""

    python -m mkdocs build --clean

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "[OK] Documentation built in site/ folder" -ForegroundColor Green
        Write-Host "    Open site\index.html in browser" -ForegroundColor Green

        # Ask if user wants to open browser
        $openBrowser = Read-Host "Open in browser? (y/n)"
        if ($openBrowser -eq 'y' -or $openBrowser -eq 'Y') {
            $indexPath = Join-Path $PWD "site\index.html"
            if (Test-Path $indexPath) {
                & "cmd" /c "start $indexPath"
            }
            else {
                Write-Host "[WARN] File not found: $indexPath" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host ""
        Write-Host "[ERROR] Build failed with errors." -ForegroundColor Red
        exit 1
    }
}