---
name: project_structure
description: Структура каталогов проекта, назначении корневых файлов и конфигураций. Используется для навигации по коду и понимания окружения.
invokable: true
---

## Структура проекта
| Путь | Назначение |
|------|------------|
| `README.md` | Главная документация, описание запуска |
| `env.example` | Пример переменных окружения |
| `src/` | Исходный код (Python package `alphameterqc`) |
| `src/alphameterqc/` | Основной пакет приложения |
| `tests/` | Тесты (структура повторяет `src/`) |
| `docs/` | Документация (specs, adr, api, templates) |
| `docs/templates/` | Шаблоны документов (ADR, code review, specs и т.д.) |
| `docs/specs/` | Спецификации по модулям (login_dialog, db, api) |
| `scripts/` | Скрипты окружения, сборки, CI-хелперы |
| `examples/` | Примеры использования (скрипты для демонстрации) |
| `pyproject.toml` | Конфиг проекта (зависимости, линтеры, тесты) |
| `mkdocs.yml` | Конфиг документации (навигация, темы) |
| `.github/workflows/` | CI/CD пайплайны (GitHub Actions) |
| `.devcontainer/` | Настройки IDE (VS Code) и контейнеризации |
| `.gitignore`, `.dockerignore`, `.pre-commit-config.yaml` | Конфигурация окружения (git, docker, pre-commit) |
