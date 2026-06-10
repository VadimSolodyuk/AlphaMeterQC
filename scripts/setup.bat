@echo off
REM Скрипт быстрой настройки проекта на новой машине (Windows)

echo Настройка проекта AlphaMeterQC...

REM 1. Проверка Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python не найден. Установите Python 3.9+
    pause
    exit /b 1
)

REM 2. Создание venv
echo Создание виртуального окружения...
python -m venv venv

REM 3. Активация venv
echo Активация venv...
call venv\Scripts\activate.bat

REM 4. Обновление pip
echo Обновление pip...
python -m pip install --upgrade pip

REM 5. Установка зависимостей
echo Установка зависимостей...
pip install -e .[dev]

REM 6. Установка pre-commit хуков
echo Установка pre-commit хуков...
pre-commit install

echo.
echo Настройка завершена!
echo Python: where python
python --version
echo.
echo Для активации venv в будущем используйте:
echo    venv\Scripts\activate.bat
pause