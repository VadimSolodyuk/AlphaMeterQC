# Инвентаризация конфигурации DevOps

## Единая таблица конфигурационных файлов и скриптов

| Категория               | Файл / Скрипт                                   | Назначение                                                                 | Триггеры (CI/CD)          | Задачи (CI/CD)                              |
|-------------------------|-------------------------------------------------|----------------------------------------------------------------------------|---------------------------|---------------------------------------------|
| **CI/CD**               | `.github/workflows/ci.yml`                      | Непрерывная интеграция – запуск тестов при push/PR в main                  | push, pull_request (main) | линтинг, тестирование, сборка документации  |
|                         | `.github/workflows/docs.yml`                    | Развёртывание документации на GitHub Pages при push в main                 | push (main)               | сборка документации, развёртывание          |
| **Окружение**           | `scripts/setup.sh`                              | Создание виртуального окружения Python (Linux/macOS)                       | —                         | —                                           |
|                         | `scripts/setup.bat`                             | Создание виртуального окружения Python (Windows)                           | —                         | —                                           |
|                         | `scripts/setup.ps1`                             | Создание виртуального окружения Python (PowerShell)                        | —                         | —                                           |
|                         | `scripts/activate_venv.sh`                      | Активация виртуального окружения (Linux/macOS)                             | —                         | —                                           |
|                         | `scripts/activate_venv.bat`                     | Активация виртуального окружения (Windows)                                 | —                         | —                                           |
|                         | `scripts/check_env.sh`                          | Проверка наличия необходимых переменных окружения                          | —                         | —                                           |
|                         | `scripts/settings.md`                           | Документация по настройке окружения                                        | —                         | —                                           |
|                         | `env.example`                                   | Шаблон переменных окружения (копировать в `.env`)                          | —                         | —                                           |
| **Контейнеризация**     | `.devcontainer/devcontainer.json`               | Конфигурация Dev Container для VS Code Remote – Containers                 | —                         | —                                           |
|                         | `.devcontainer/Dockerfile`                      | Docker-образ для контейнера разработки                                     | —                         | —                                           |
|                         | `.dockerignore`                                 | Исключения для Docker (не включать в образ)                                | —                         | —                                           |
| **Документация**        | `mkdocs.yml`                                    | Конфигурация MkDocs (тема, навигация, плагины)                             | —                         | —                                           |
|                         | `scripts/build_docs.sh`                         | Локальная сборка документации (Linux/macOS)                                | —                         | —                                           |
|                         | `scripts/build_docs.bat`                        | Локальная сборка документации (Windows)                                    | —                         | —                                           |
|                         | `scripts/build_docs.ps1`                        | Локальная сборка документации (PowerShell)                                 | —                         | —                                           |
|                         | `README.md`                                     | Основной файл описания проекта (установка, использование)                  | —                         | —                                           |
|                         | `todo.md`                                       | Список задач и планов развития                                             | —                         | —                                           |
| **Тестирование**        | `scripts/run_tests.sh`                          | Запуск всех тестов (pytest + отчёт о покрытии)                             | —                         | —                                           |
|                         | `tests/`                                        | Директория с тестами (зеркалирует `src/`)                                  | —                         | —                                           |
| **Pre-commit**          | `.pre-commit-config.yaml`                       | Конфигурация pre-commit хуков (black, flake8, mypy, isort)                 | —                         | —                                           |
| **Инфраструктура**      | `.lingma/rules/optimize_context.md`             | Правила оптимизации контекста для Lingma                                   | —                         | —                                           |
|                         | `examples/ollama_example.py`                    | Пример использования Ollama                                                | —                         | —                                           |
|                         | `examples/test_ollama.py`                       | Тестовый скрипт для Ollama                                                 | —                         | —                                           |
|                         | `pyproject.toml`                                | Конфигурация проекта (зависимости, метаданные, инструменты)                | —                         | —                                           |
| **Резервное копирование БД** | `docs/specs/db/16_backup_script.sh`        | Резервное копирование PostgreSQL                                           | —                         | —                                           |
|                         | `docs/specs/db/17_restore_script.sh`            | Восстановление PostgreSQL                                                  | —                         | —                                           |

## Примечания

- Для CI/CD используются GitHub Secrets (`API_KEY`, `DATABASE_URL` и т.д.).
- Мониторинг и логирование пока не настроены (планируется structlog + health endpoints).
- Dockerfile для production отсутствует – рекомендуется добавить.
- Файлы `scripts/settings.md` и `.lingma/rules/` добавлены как вспомогательные для разработки.

---

*Документ актуален на момент последнего обновления дерева файлов.*