#!/bin/bash
# Скрипт быстрой настройки проекта на новой машине (Linux/macOS)

echo "🚀 Настройка проекта AlphaMeterQC..."

# 1. Проверка Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 не найден. Установите Python 3.9+"
    exit 1
fi

# 2. Создание venv
echo "📦 Создание виртуального окружения..."
python3 -m venv venv

# 3. Активация venv
echo "🔧 Активация venv..."
source venv/bin/activate

# 4. Обновление pip
echo "⬆️  Обновление pip..."
pip install --upgrade pip

# 5. Установка зависимостей
echo "📚 Установка зависимостей..."
pip install -e .[dev]

# 6. Установка pre-commit хуков
echo "🪝 Установка pre-commit хуков..."
pre-commit install

# 7. Проверка
echo ""
echo "✅ Настройка завершена!"
echo "📍 Python: $(which python)"
echo "📦 Версия: $(python --version)"
echo ""
echo "💡 Для активации venv в будущем используйте:"
echo "   source venv/bin/activate"