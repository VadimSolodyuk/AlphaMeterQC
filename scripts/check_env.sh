#!/bin/bash

echo " Проверка окружения AlphaMeterQC..."
echo ""

# 1. Проверка Python
echo "1. Версия Python:"
python --version
echo ""

# 2. Проверка импорта пакета
echo "2. Проверка импорта пакета:"
python -c "import alphameterqc; print('✅ alphameterqc импортирован')" || echo "❌ Ошибка импорта"
echo ""

# 3. Проверка зависимостей
echo "3. Проверка зависимостей:"
python -c "import black; print(f'✅ black {black.__version__}')" || echo "❌ black не установлен"
python -c "import isort; print(f'✅ isort {isort.__version__}')" || echo "❌ isort не установлен"
python -c "import flake8; print(f'✅ isort {isort.__version__}')" || echo "❌ isort не установлен"
mypy --version | grep -q "mypy" && echo "✅ $(mypy --version)" || echo "❌ mypy не установлен"
echo ""

# 4. Проверка Git
echo "4. Проверка Git:"
git --version
git config user.name
git config user.email
echo ""

echo "✅ Проверка завершена!"