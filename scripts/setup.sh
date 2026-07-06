#!/bin/bash
# Скрипт быстрой и надежной настройки проекта AlphaMeterQC
# Артефакт: setup.sh_2026-06-13_12:00

# 1. Строгий режим Bash (Best Practice для DevOps и CI/CD)
# -e: немедленный выход при ошибке любой команды (fail-fast)
# -u: ошибка при использовании неинициализированных переменных (защита от опечаток)
# -o pipefail: ошибка в любой части конвейера (|) прерывает весь скрипт, а не только последнюю команду
set -euo pipefail

# 2. Цвета для вывода (улучшает читаемость логов в терминале)
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color (сброс цвета)

# 3. Конфигурация проекта
VENV_DIR="venv"
MIN_PYTHON_MAJOR=3
MIN_PYTHON_MINOR=9

echo -e "${BLUE}🚀 Начало настройки проекта AlphaMeterQC...${NC}"

# 4. Проверка наличия Python 3
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Ошибка: python3 не найден в системе.${NC}"
    echo "Установите Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR}+ перед запуском этого скрипта."
    exit 1
fi

# 5. Проверка версии Python (извлекаем мажорную и минорную версии, например: "3 10")
PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major} {sys.version_info.minor}")')
read -r PY_MAJOR PY_MINOR <<< "$PYTHON_VERSION"

if [ "$PY_MAJOR" -lt "$MIN_PYTHON_MAJOR" ] || ([ "$PY_MAJOR" -eq "$MIN_PYTHON_MAJOR" ] && [ "$PY_MINOR" -lt "$MIN_PYTHON_MINOR" ]); then
    echo -e "${RED}❌ Ошибка: Требуется Python ${MIN_PYTHON_MAJOR}.${MIN_PYTHON_MINOR} или выше.${NC}"
    echo "Текущая версия: ${PY_MAJOR}.${PY_MINOR}"
    exit 1
fi
echo -e "${GREEN}✅ Python версии ${PY_MAJOR}.${PY_MINOR} найден.${NC}"

# 6. Создание виртуального окружения (Идемпотентность)
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}📦 Создание виртуального окружения в '${VENV_DIR}'...${NC}"
    python3 -m venv "$VENV_DIR"
else
    echo -e "${GREEN}ℹ️  Виртуальное окружение '${VENV_DIR}' уже существует. Пропуск создания.${NC}"
fi

# 7. Обновление pip и установка зависимостей
# ВАЖНО: Мы используем прямой путь к исполняемым файлам внутри venv (${VENV_DIR}/bin/...).
# Это гарантирует, что команды выполняются именно в целевом окружении, 
# независимо от того, был ли выполнен 'source activate' в текущей оболочке.
echo -e "${YELLOW}⬆️  Обновление pip внутри venv...${NC}"
"${VENV_DIR}/bin/python" -m pip install --upgrade pip

echo -e "${YELLOW}📚 Установка зависимостей проекта (режим разработки)...${NC}"
"${VENV_DIR}/bin/python" -m pip install -e .[dev]

# 8. Установка pre-commit хуков
echo -e "${YELLOW}🪝 Установка pre-commit хуков...${NC}"
"${VENV_DIR}/bin/pre-commit" install

# 9. Итоговое сообщение
echo ""
echo -e "${GREEN}✅ Настройка проекта успешно завершена!${NC}"
echo "📍 Интерпретатор venv: $("${VENV_DIR}/bin/python" -c 'import sys; print(sys.executable)')"
echo "📦 Версия Python: $("${VENV_DIR}/bin/python" --version)"
echo ""
echo -e "${BLUE}💡 Следующий шаг: активируйте окружение для начала работы:${NC}"
echo "   source ${VENV_DIR}/bin/activate"
echo ""