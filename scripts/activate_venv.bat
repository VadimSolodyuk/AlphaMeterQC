@echo off
REM Скрипт активации venv для Windows
echo Activating virtual environment...
call "%~dp0..\venv\Scripts\activate.bat"
echo.
echo venv activated!
echo Python: where python
python --version