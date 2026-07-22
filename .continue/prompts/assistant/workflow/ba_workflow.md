---
name: BA_workflow
description: Инструкция по ведению workflow + Правила именования и расположения артефактов.
invokable: true
---

## Workflow этап + правила именования артефактов
| Этап | Роль | Ключевые действия | Создаваемые артефакты | Правило именования | Пути размещения | Шаблон |
|------|------|-------------------|-----------------------|--------------------|-----------------|--------|
| **1. Business Analysis** | BA | Формализовать требования… | Концепция, Stakeholders Requirements, User Stories, Use cases, SRS, Technical Specification, UI Design, UI Traceability, RTM, Business Process Analysis, ER Diagram, Logical Model, Normalization, API Specification | Файлы: `<номер>_<тип>_<module>_<feature>.md`; ID: `UC.LOGIN.AUTH.D1.01`, `SR-1`, `F-01` | `docs/specs/<module>/`; `docs/specs/api/` | `docs/templates/` + `01_concept-template.md`, `02_stakeholders_requirements-template.md`, `03_user_stories-template.md`, `04_srs-template.md`, `05-1_UC-template.md`, `05_use_cases-template.md`, `06_rtm-template.md`, `08_technical_specification-template.md`, `09_ui_design-template.md`, `10_ui_traceability-template.md` |

**Версионирование спецификаций** — семантическое `MAJOR.MINOR`. При каждом изменении: увеличивается версия, обновляется `date`, в конец файла добавляется запись в CHANGELOG (колонки: Версия, Дата, Тип, Описание). Версия спецификации должна быть согласована с версией соответствующего ADR (даты обновления совпадают).