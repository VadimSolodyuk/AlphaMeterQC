# AlphaMeterQC

[![CI/CD Pipeline](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/ci.yml/badge.svg)](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/ci.yml)
[![Docs](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/docs.yml/badge.svg)](https://github.com/VadimSolodyuk/AlphaMeterQC/actions/workflows/docs.yml)

**Версия:** 0.1.0  
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
- ✅ Автоматические тесты; результаты и границы покрытия — в разделе «Тестирование»

---

## Требования

- Python >= 3.12; базовая версия разработки — 3.12
- CustomTkinter >= 5.2.0
- Windows 10/11 или Linux Ubuntu 20.04+

Автоматические тесты локально пройдены на Linux с Python 3.12.3.
Версии 3.13 и 3.14 включены в матрицу CI для проверки совместимости;
их наличие в матрице само по себе не подтверждает успешное прохождение.

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

Собирается стартовый каркас AlphaMeterQC, а не отдельный исполняемый
файл диалога. Сборку выполняйте на целевой ОС: Windows-версию —
на Windows, Linux-версию — на Linux.

Из корня репозитория в активированном виртуальном окружении:

```bash
python -m pip install -e .
python -m pip install pyinstaller
python -m PyInstaller --clean --noconfirm --onefile --name AlphaMeterQC --collect-all customtkinter src/alphameterqc/__main__.py
```

`alphameterqc/__main__.py` использует абсолютный импорт `app.main`.
Отдельный launcher не требуется. Параметр `--collect-all customtkinter`
включает ресурсы GUI. Консольный режим пока сохраняется для диагностики;
параметры подключения и пароль приложение в stdout/stderr не выводит.

Ожидаемые файлы:
- Linux: `dist/AlphaMeterQC`;
- Windows: `dist/AlphaMeterQC.exe`.

CI использует эту же точку входа. Артефакты называются
`AlphaMeterQC-ubuntu-latest` и `AlphaMeterQC-windows-latest`.

Не добавляйте `build/`, `dist/` и создаваемый `AlphaMeterQC.spec`
в коммит без отдельной необходимости.

Инструкция не подтверждает успешный запуск бинарников: требуется
проверка в целевой среде вне дерева исходников.

---

## Использование

### Запуск AlphaMeterQC

```bash
python -m alphameterqc
```

Или запустите собранный `AlphaMeterQC` / `AlphaMeterQC.exe`.
Приложение первым открывает диалог параметров подключения через
библиотечный API, без subprocess и JSON-обмена.

Это стартовый каркас: после подтверждения ввода он сообщает в stderr,
что подключение к БД и основной интерфейс ещё не реализованы,
и завершается с кодом 0. Отмена также завершает приложение с кодом 0.
Параметры подключения и пароль не печатаются. Существующее сохранение
параметров без пароля внутри диалога не меняется.

Ограничение текущего API: диалог возвращает `None` и при отмене,
и при обработанной внутренней ошибке. Эти исходы приложение пока
не различает. Исключение, вышедшее за пределы API, даёт код 1
и общее сообщение без текста исключения.

Библиотечный и subprocess-интерфейсы самого `login_dialog` сохранены
для совместимости. Сборка самостоятельного бинарника диалога
в текущем CI больше не выполняется.

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

Локальная проверка от 07.11.2026: Linux, Python 3.12.3,
коммит `878779f`. Команда: `python -m pytest -v`.

Собрано 126 тестовых случаев: 125 успешно, 1 Windows-специфичный
тест пропущен.

| Модуль | Покрытие |
|--------|----------|
| `model.py` | 91% |
| `controller.py` | 100% |
| `api.py` | 80% |
| Учитываемый код в целом | 92,61% |

Значения по модулям округлены в отчёте pytest-cov.
Порог покрытия 80% достигнут.

Из измерения исключены `prototype.py`, `__main__.py`, `view.py`
и `ai_service.py`. Результат не характеризует покрытие всего
приложения и не подтверждает ручную проверку GUI или бинарников.

---

## CI/CD

При push в ветку `main` автоматически запускается:

1) **Тесты** — pytest на Python 3.12, 3.13, 3.14
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

AlphaMeterQC распространяется на индивидуальных условиях,
изложенных в файле `LICENSE` (редакция 1.0).

Без отдельного согласования разрешаются использование,
изменение и распространение программы исключительно
в личных и учебных некоммерческих целях при соблюдении
условий `LICENSE`.

Любое коммерческое использование, включая использование
внутри коммерческой организации для её собственных нужд,
требует предварительного письменного разрешения
правообладателя.

При распространении необходимо сохранять уведомления
об авторских правах и полный текст условий, обозначать
внесённые изменения и не выдавать изменённую версию
за оригинальную версию автора.

Новые условия не отменяют права, ранее правомерно
полученные по иным условиям лицензирования.

Условия сторонних компонентов определяются
их собственными лицензиями.

---

## Контакты

**Автор:** Солодюк В.Л.  
**Репозиторий:** https://github.com/VadimSolodyuk/AlphaMeterQC  
**Документация:** https://vadimsolodyuk.github.io/AlphaMeterQC/  
**Проект:** AlphaMeterQC — система анализа и контроля
данных АСКУЭ