@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================
REM   AlphaMeterQC Documentation Build Script
REM   Run: scripts\build_docs.bat
REM   Development mode: scripts\build_docs.bat serve [port]
REM ============================================

REM Обычная сборка (спросит про открытие браузера)
REM scripts\build_docs.bat

REM Режим разработки с автооткрытием браузера
REM scripts\build_docs.bat serve

REM Режим разработки на порту 9000
REM scripts\build_docs.bat serve 9000

REM Без автооткрытия браузера
REM scripts\build_docs.bat -nobrowser
REM scripts\build_docs.bat serve -nobrowser
REM scripts\build_docs.bat serve 9000 -nobrowser


REM Parse arguments
set "MODE=build"
set "PORT=8000"
set "NO_BROWSER=0"

if "%~1"=="" goto check_venv
if /i "%~1"=="serve" (
    set "MODE=serve"
    if not "%~2"=="" (
        if /i "%~2"=="-nobrowser" (
            set "NO_BROWSER=1"
        ) else (
            set "PORT=%~2"
            if /i "%~3"=="-nobrowser" set "NO_BROWSER=1"
        )
    )
    goto check_venv
)
if /i "%~1"=="-nobrowser" (
    set "NO_BROWSER=1"
    goto check_venv
)

:check_venv
REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found.
    echo Run scripts\setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if MkDocs is installed
python -m mkdocs --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] MkDocs not installed.
    echo Run: pip install -e .[dev]
    pause
    exit /b 1
)

if "%MODE%"=="serve" (
    goto serve_mode
) else (
    goto build_mode
)

:serve_mode
echo ============================================
echo   MkDocs Documentation Server
echo ============================================
echo.
echo [INFO] Starting dev server on port %PORT%...
echo Server URL: http://localhost:%PORT%
echo Press Ctrl+C to stop
echo.

if "%NO_BROWSER%"=="1" (
    echo [INFO] Auto-open browser disabled
) else (
    echo [INFO] Opening browser...
    timeout /t 3 /nobreak >nul
    start "" "http://localhost:%PORT%"
)

echo.
python -m mkdocs serve --dev-addr "127.0.0.1:%PORT%"
goto end

:build_mode
echo ============================================
echo   MkDocs Documentation Build
echo ============================================
echo.
echo [INFO] Building documentation...
echo.

python -m mkdocs build --clean

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed with errors.
    pause
    exit /b 1
)

echo.
echo [OK] Documentation built in site/ folder
echo     Open site\index.html in browser
echo.

if "%NO_BROWSER%"=="1" (
    goto end
)

REM Ask user if they want to open browser
set /p OPEN_BROWSER="Open in browser? (y/n): "
if /i "%OPEN_BROWSER%"=="y" (
    if exist "site\index.html" (
        start "" "site\index.html"
    ) else (
        echo [WARN] File not found: site\index.html
    )
)

goto end

:end
endlocal