---
name: Rules System Overview
alwaysApply: false
description: Общая информация о системе правила их автоматического включения
---

# Система правил

## 📋 Доступные правила

### 1. **Project Manager** (`01-project_manager.md`)
**Включается вручную** — координация цикла разработки, контроль качества
- **Ключевые принципы:** работа с `temp/`, поэтапный процесс, передача контекста
- **Ограничения:** ЗАПРЕЩЕНО пропускать QA, коммитить без документации, менять архитектуру без согласования

### 2. **Business Analyst** (`02-business_analyst.md`)
**Автоматически:** `docs/specs/**/*.md` — требования, use cases, RTM
- **Ключевые принципы:** стандарты документирования (шаблоны, нумерация UC.*), трассировка требований
- **Ограничения:** ЗАПРЕЩЕНО пропускать согласование требований, допускать неоднозначные формулировки

### 3. **Architect** (`03-architect.md`)
**Автоматически:** `docs/specs/**/*.md` — архитектура, паттерны, ADR
- **Ключевые принципы:** SOLID, DRY, KISS, YAGNI, GRASP, SSOT, POLA
- **Ограничения:** ЗАПРЕЩЕНО нарушать принципы проекта, over-engineering

### 4. **Developer-Mentor** (`04-developer_mentor.md`)
**Автоматически:** `src/**/*.*` — код, best practices
- **Ключевые принципы:** Clean Code, SOLID, DRY, KISS, YAGNI, Fail Fast, Boy Scout Rule
- **Ограничения:** ЗАПРЕЩЕНО использовать deprecated методы, хардкодить секреты, молча менять архитектуру

### 5. **QA-Specialist** (`05-qa_specialist.md`)
**Автоматически:** `tests/**/*.*` или `src/**/*.*` — безопасность, тесты
- **Ключевые принципы:** Shift Left, 2-3 edge cases на функцию, проверка deprecated и обработки ошибок
- **Ограничения:** ЗАПРЕЩЕНО пропускать deprecated методы, игнорировать уязвимости

### 6. **DevOps** (`06-devops.md`)
**Автоматически:** `pyproject.toml`, `scripts/**/*.*`, `README.md`, `mkdocs.yml` — окружение, CI/CD
- **Ключевые принципы:** Conventional Commits, Git-процессы, `pyproject.toml`, `pyinstaller_specs/`
- **Ограничения:** ЗАПРЕЩЕНО нарушать структуру проекта

## 🔄 Workflow

```
PM → BA (анализ) → Architect (проектирование) → Mentor (реализация) → QA (проверка) → DevOps (документация/окружение) → PM (сверка)
```

Промежуточные результаты → `docs/specs/temp/[тип]-[тема]-[статус].md`
(создаются копированием соответствующего шаблона из `docs/specs/templates/`)

Шаблоны документов → `docs/specs/templates/`:
- **Спецификации:** ADR, feature-spec, code-review, workflow
- **Межэтапная передача:** architecture-output, implementation-output, qa-review-output, documentation-output

## 💡 Советы

1. **Новые фичи** → используй `Project Manager`
2. **Требования/спецификации** → создавай файл в `docs/specs/` — **BA** подключится автоматически
3. **Архитектура** → создавай файл в `docs/specs/` — **Architect** подключится автоматически
4. **Код** → **Developer-Mentor** подключится при работе с `src/`
5. **Проверка** → обращайся к **QA-Specialist** перед коммитом
6. **Документация/окружение** → **DevOps** подключится при работе с README/mkdocs/pyproject.toml


