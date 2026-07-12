# AlphaMeterQC

[![CI/CD Pipeline](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/ci.yml/badge.svg)](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/ci.yml)
[![Docs](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/docs.yml/badge.svg)](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/docs.yml)

**Версия:** 0.2.0  
**Статус:** Разработка  
**Автор:** Солодюк В.Л.  
**Дата:** 2026-06-11  

AlphaMeterQC — программное средство для анализа и контроля
своевременности поступления, полноты и корректности данных,
собранных со счётчиков электрической энергии и хранящихся в
базе данных (Oracle) ПО «АльфаЦЕНТР».

Разработка ведётся в рамках выпускной квалификационной работы
по специальности 09.02.07 «Информационные системы и
программирование».

 **Веб-документация проекта:**
[vadimsolodyuk.github.io/AlphaMeterQC](https://vadimsolodyuk.github.io/AlphaMeterQC/)

---

## Модули системы

| № | Модуль | Статус | Описание |
|---|--------|--------|----------|
| 1 | `login_dialog` | ✅ Готов | Диалог ввода параметров подключения к БД |
| 2 | `data_extractor` | 🚧 Планируется | Извлечение данных из Oracle |
| 3 | `analytics` | 🚧 Планируется | Анализ своевременности и полноты |
| 4 | `reporting` |  Планируется | Формирование отчётности |

---

## Модуль `login_dialog`

Первый реализованный модуль системы. Предоставляет
графический интерфейс для ввода данных
подключения к базе данных Oracle ПО «АльфаЦЕНТР».

### Возможности

- ✅ Современный интерфейс на CustomTkinter (светлая тема)
- ✅ Окно открывается по центру экрана
- ✅ Валидация IPv4 и DNS в реальном времени
- ✅ Маскировка пароля
- ✅ Сохранение параметров между сессиями (JSON)
- ✅ Атомарная запись через `os.replace()`
- ✅ Два режима интеграции: библиотека и subprocess
- ✅ Кроссплатформенность (Windows, Linux)
- ✅ Покрытие тестами 85%+

---

## Требования

- Python 3.9 – 3.12
- CustomTkinter >= 5.2.0
- Windows 10/11 или Linux Ubuntu 20.04+

---

## Установка

### Из исходников

```bash
git clone https://github.com/VadimSolodyuk/AlphaMeterQC.git
cd AlphaMeterQC

python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

pip install -e .[dev]
```

### Через PyInstaller (единый исполняемый файл)

Проект содержит готовый spec-файл `login_dialog.spec`,
который автоматически определяет путь к CustomTkinter
и корректно работает на любой платформе.

```bash
pip install pyinstaller
pyinstaller login_dialog.spec
```

Готовый файл будет в папке `dist/`:
- Linux: `dist/login_dialog`
- Windows: `dist/login_dialog.exe`

---

## Использование

### Режим библиотеки

```python
from alphameterqc.login_dialog import show_dialog

result = show_dialog(
    default_ip="192.168.1.1",
    default_port=1521,
    default_username="admin",
    default_service_name="ORCL",
)

if result:
    print(f"Подключение к {result['ip']}:{result['port']}")
else:
    print("Пользователь отменил ввод")
```

### Режим subprocess

```python
import subprocess
import json

result = subprocess.run(
    ["python", "-m", "alphameterqc.login_dialog"],
    capture_output=True,
    text=True,
)

output = json.loads(result.stdout)

if output["status"] == "success":
    data = output["data"]
    print(f"Подключение к {data['ip']}:{data['port']}")
elif output["status"] == "cancelled":
    print("Пользователь отменил ввод")
```

---

## Хранение конфигурации

Параметры подключения (кроме пароля) сохраняются между
сессиями:

| ОС | Путь |
|----|------|
| Windows | `%LOCALAPPDATA%\alphameterqc\connection.json` |
| Linux | `~/.config/alphameterqc/connection.json` |

⚠️ Пароль никогда не сохраняется на диск (NF-3a).

---

## Тестирование

```bash
scripts/run_tests.sh
```

### Метрики

| Модуль | Покрытие |
|--------|----------|
| `model.py` | 89% |
| `controller.py` | 100% |
| `api.py` | 80% |
| `view.py` | исключён (GUI) |
| **Общее** | **85%+** |

Всего тестов: **127** (unit + integration).

---

## CI/CD

При push в ветку `main` автоматически запускается:

1) **Тесты** — pytest на Python 3.10, 3.11, 3.12
2) **Линтинг** — black, isort, mypy strict, flake8
3) **Документация** — сборка и деплой на GitHub Pages
4) **Сборка** — PyInstaller для Windows и Linux

---

## Документация

Полная документация в `docs/specs/login_dialog/`:

1. Концепция (`01_concept.md`)
2. Требования стейкхолдеров (`02_stakeholders_requirements.md`)
3. Пользовательские истории (`03_user_stories.md`)
4. SRS (`04_srs.md`)
5. Варианты использования (`05_use_cases.md`)
6. Детальные UC (`05-1` — `05-5`)
7. Матрица трассировки (`06_rtm.md`)
8. Модель предметной сферы (`07_domain_model.md`)
9. Техническое задание (`08_technical_specification.md`)
10. Дизайн UI (`09_ui_design.md`)
11. Трассировка UI (`10_ui_traceability.md`)

### Веб-версия

```bash
scripts/build_docs.sh
# или
mkdocs build --clean && mkdocs serve
```

Онлайн: [vadimsolodyuk.github.io/AlphaMeterQC](https://vadimsolodyuk.github.io/AlphaMeterQC/)

---

## Разработка

### Требования к коду

- **PEP 8** — стиль кодирования (flake8)
- **mypy strict mode** — статическая проверка типов
- **Black** — автоформатирование (88 символов)
- **Google-style docstrings**

### Pre-commit хуки

```bash
pre-commit install
pre-commit run --all-files
```

### Dev Container

```bash
F1 → Dev Containers: Reopen in Container
```

Контейнер включает Python 3.12, все зависимости,
расширения VS Code (Python, Black, MyPy, Flake8).

---

## Планы развития

В рамках выпускной квалификационной работы планируется
разработка дополнительных модулей системы:

1) **data_extractor** — извлечение данных из Oracle с
   использованием библиотеки `oracledb`;
2) **analytics** — анализ своевременности и полноты
   поступления показаний с помощью `Pandas`, `NumPy`,
   `Matplotlib`, `Plotly`;
3) **reporting** — формирование отчётности в форматах
   PDF и Excel;
4) **CI/CD** — расширение конвейера автосборкой
   исполняемых файлов при релизах.

---

## Лицензия

MIT License. См. файл `LICENSE` для подробностей.

---

## Контакты

**Автор:** Солодюк В.Л.  
**Репозиторий:** https://github.com/VadimSolodyuk/AlphaMeterQC  
**Документация:** https://vadimsolodyuk.github.io/AlphaMeterQC/  
**Проект:** AlphaMeterQC — система анализа и контроля
данных АСКУЭ