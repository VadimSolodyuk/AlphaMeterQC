---
name: dev_env_setup
description: Настройка виртуального окружения (локальная разработка)
invokable: true
---

## Определение используемого инструмента
Проверь наличие файлов в корне проекта:
- `pyproject.toml` — может содержать конфигурацию для любого инструмента
- `requirements.txt` — стандартный pip/venv
- `poetry.lock` / `[tool.poetry]` в pyproject.toml — Poetry
- `Pipfile` / `Pipfile.lock` — Pipenv
- `uv.lock` / `[tool.uv]` в pyproject.toml — uv

## Рекомендуемые команды

### venv
```bash
# Linux/macOS
source venv/bin/activate && python ...
# Windows (cmd)
venv\Scripts\activate.bat && python ...
# Windows (PowerShell)
venv\Scripts\Activate.ps1 && python ...
```
### uv
```bash
uv run python ...
```
### poetry
```bash
poetry run python ...
```
### pipenv
```bash
pipenv run python ...
```

## Правила
1. Никогда не предполагай инструмент — проверяй файлы проекта.
2. Предпочитай `run`-команды прямой активации оболочки.
3. Не вставляй команды активации в Python-код — только для терминала.
4. Если окружение отсутствует, предложи команду создания:
   - venv: `python -m venv venv`
   - uv: `uv venv`
   - poetry: `poetry install`
   - pipenv: `pipenv install`
5. В Dev Container эта проверка не нужна — среда уже настроена.