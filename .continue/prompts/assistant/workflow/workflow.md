---
name: workflow
description: Инструкция по ведению workflow + Правила именования и расположения артефактов.
invokable: true
---

## Workflow этап + правила именования артефактов
| Этап | Роль | Ключевые действия | Создаваемые артефакты | Правило именования | Пути размещения | Шаблон |
|------|------|-------------------|-----------------------|--------------------|-----------------|--------|
| **4. Quality Assurance** | QA | Проверить код, разработать тест-кейсы, автоматизировать регрессию | Тест-кейсы, Code Review Report, отчёты, Load Testing Results, Load Test Data, Bottleneck Analysis | Stage‑output: `<module>_<feature>_qa_<дата>.md` | Тест-кейсы → `docs/specs/<module>/`; Автотесты → `tests/`; Отчёты → `docs/temp/<module>/` | `docs/templates/` + `code-review-template.md`, `stage-output-template.md` |
| **5. Documentation & Environment** | DevOps | Обновить README, mkdocs, CI/CD, зависимости | Документация, конфиги, скрипты, примеры, Deployment Guide, Optimization Queries, Backup Script, Restore Script, Security Policy, DevOps Config Inventory | Stage‑output: `<module>_<feature>_docs_<дата>.md` | Конфиги → см. `docs/specs/devops_config_inventory.md` | `docs/templates/stage-output-template.md` |

**Дополнительно:**
- **Версионирование спецификаций** — семантическое `MAJOR.MINOR`. При каждом изменении: увеличивается версия, обновляется `date`, в конец файла добавляется запись в CHANGELOG (колонки: Версия, Дата, Тип, Описание). Версия спецификации должна быть согласована с версией соответствующего ADR (даты обновления совпадают).
- **Временные файлы** (stage‑output) хранятся в: `docs/temp/`; `docs/temp/<module>/`. После завершения фичи архивируются или удаляются по согласованию.

