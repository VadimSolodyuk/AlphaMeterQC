---
name: Project Architecture
alwaysApply: false
description: Project Architecture
---

  ## Архитектура проекта
  Проект имеет следующую структуру:
- Документация и спецификации в `docs/specs/`
- Исходный код в `src/`
- Тесты в `tests/`
- Скрипты автоматизации в `scripts/`
- Конфигурация сборки PyInstaller в `pyinstaller_specs/`
- Сайт документации в `site/` (генерируется через MkDocs)
- Примеры использования в `examples/`
- CI/CD конфигурация в `.github/` (GitHub Actions)
- Конфигурация Dev Container в `.devcontainer/` (Docker)
- Настройки IDE в `.vscode/` (VS Code)
- Pre-commit хуки в `.pre-commit-config.yaml`
- Конфигурация документации MkDocs в `mkdocs.yml`
- Основная документация в `README.md`
- Пример переменных окружения в `env.example`
- Трекер задач в `todo.md`
- Виртуальное окружение в `venv/` (если не в container)
- Конфигурация проекта в `pyproject.toml`
