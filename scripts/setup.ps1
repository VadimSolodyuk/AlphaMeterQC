# AlphaMeterQC project setup script for Windows PowerShell
# Run: .\scripts\setup.ps1

# Configure UTF-8 encoding
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$ErrorActionPreference = "Stop"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  AlphaMeterQC Project Setup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "[INFO] Creating virtual environment..." -ForegroundColor Gray
    python -m venv venv
}

# Activate virtual environment
Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Gray
& "venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "[INFO] Upgrading pip..." -ForegroundColor Gray
python -m pip install --upgrade pip

# Install project dependencies
Write-Host "[INFO] Installing project dependencies..." -ForegroundColor Gray
pip install -e .[dev]

# Install pre-commit hooks
Write-Host "[INFO] Installing pre-commit hooks..." -ForegroundColor Gray
pre-commit install

# Final message
Write-Host ""
Write-Host "[OK] Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  Run tests:       .\scripts\run_tests.ps1" -ForegroundColor Gray
Write-Host "  Serve docs:      .\scripts\build_docs.ps1 -Serve" -ForegroundColor Gray
Write-Host "  Build docs:      .\scripts\build_docs.ps1" -ForegroundColor Gray
Write-Host ""