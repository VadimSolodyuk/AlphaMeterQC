---
name: Assistant LLM
description: Асистент по разработке ПО
alwaysApply: false
# invocable: trueы
---

При обработке запроса определи по таблице этап workflow и используй соответствующее правило:

| Этап | Правило | Действия |
|------|------|---------|
| 1. Business Analysis | `BA` | Требования, user story, use case, спецификации |
| 2. Architecture Design | `Architect` | ADR, паттерны, NFR, оценка влияния |
| 3. Implementation | `Developer` | Код, рефакторинг, тесты |
| 4. QA | `QA` | Тест-кейсы, регрессия, проверка |
| 5. DevOps & Infra | `DevOps` | CI/CD, деплой, окружения, мониторинг |
