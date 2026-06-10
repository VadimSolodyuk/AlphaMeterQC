#!/bin/bash
# Скрипт для локальной сборки документации из Markdown-артефактов и Python Docstrings.
# Работает полностью офлайн.

echo "📚 Сборка локальной документации (MkDocs)..."

# Переходим в папку docs, где лежит mkdocs.yml
# cd docs

# Собираем статический сайт в папку site/
mkdocs build --clean

echo "✅ Документация собрана в папке docs/site/"
echo "💡 Чтобы просмотреть её в браузере, запусти: mkdocs serve"