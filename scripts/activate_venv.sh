#!/bin/bash
# Скрипт активации venv для Linux/macOS

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "🔧 Активация виртуального окружения..."
source "$PROJECT_ROOT/venv/bin/activate"

echo "✅ venv активировано!"
echo "📍 Python: $(which python)"
echo "📦 Версия: $(python --version)"