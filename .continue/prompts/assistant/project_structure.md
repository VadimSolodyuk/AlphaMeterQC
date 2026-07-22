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
| `docs/specs/<module>/` | Постоянные спецификации модуля (концепция, требования, use cases, SRS, RTM, доменная модель, UI-спецификация) |
| `docs/adr/` | Архитектурные решения (ADR) |
| `docs/api/` | Описание API-контрактов (если применимо) |
| `docs/templates/` | Общие шаблоны (workflow, stage-output, code-review, feature-spec) |
| `docs/temp/` | Временные артефакты, общие для проекта |
| `docs/temp/<module>/` | Временные артефакты, относящиеся к конкретному модулю |
| `scripts/` | Скрипты окружения, сборки, CI-хелперы |
| `examples/` | Примеры использования (скрипты для демонстрации) |
| `pyproject.toml` | Конфиг проекта (зависимости, линтеры, тесты) |
| `mkdocs.yml` | Конфиг документации (навигация, темы) |
| `.github/workflows/` | CI/CD пайплайны (GitHub Actions) |
| `.devcontainer/` | Настройки IDE (VS Code) и контейнеризации |
| `.gitignore`, `.dockerignore`, `.pre-commit-config.yaml` | Конфигурация окружения (git, docker, pre-commit) |
