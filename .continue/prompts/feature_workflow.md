---
name: feature_workflow
description: Инструкция для ролей по ведению workflow при средних/крупных изменениях (новая фича/модуль). Описывает этапы, передачу контекста и управление временными файлами.
invokable: true
---

## Workflow этапы

| Этап | Роль | Действия | Создаваемые артефакты |
|------|------|----------|-----------------------|
| **1. Specification & Architecture** | Spec Analyst | - Формализовать требования (следуй шаблонам из `docs/templates/specs/`)<br>- Спроектировать архитектуру (доменная модель, ADR)<br>- Обновить RTM | `docs/specs/<module>/` (концепция, use cases, SRS, ADR, RTM)<br>`docs/temp/<module>/<module>-spec-arch-<дата>.md` |
| **2. Implementation** | Code Guardian | - Реализовать код согласно спецификациям и ADR<br>- Написать unit-тесты<br>- **Обновить docstrings в коде (в соответствии с правилами Code Guardian)**<br>- **Проверить, что `mkdocs build --strict` проходит**<br>- Провести code review (если применимо) | `src/`, `tests/`<br>`docs/temp/<module>/<module>-impl-<дата>.md` |
| **3. Quality Assurance** | Code Guardian | - Проверить код на уязвимости, качество, покрытие тестами<br>- Задокументировать граничные случаи | `docs/temp/<module>/<module>-qa-<дата>.md` |
| **4. Documentation & Environment** | DevOps | - Обновить README, mkdocs, env.example<br>- Настроить CI/CD, зависимости<br>- Сгенерировать документацию | `docs/temp/<module>/<module>-docs-<дата>.md` |

> **Примечание:** Если этап не требуется (например, нет изменений окружения), stage-output всё равно создаётся с пометкой «не требуется».  
> При передаче контекста через `@context_transfer` обязательно укажите причину пропуска в поле `details`, чтобы следующая роль могла сразу приступить к работе.

## Использование `@context_transfer`
После завершения каждого этапа вызывай `@context_transfer` для передачи контекста следующей роли.  
Пример:
```text
[CONTEXT_TRANSFER]
role: Code Guardian
reason: реализация use case UC.LOGIN.D1.01
files: docs/specs/login/04-srs-login.md, docs/adr/adr-001-use-customtkinter.md
details: граничные случаи: пустой ввод, невалидный токен
[/CONTEXT_TRANSFER]
```

## Управление временными файлами
- Все stage-output хранятся в `docs/temp/`.
- После завершения фичи (все этапы пройдены) временные файлы **архивируются** в `docs/temp/archive/<module>-<дата>.zip` или удаляются по согласованию с командой.
- Постоянные спецификации остаются.