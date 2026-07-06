 # Шаблоны документации

Этот каталог содержит шаблоны для стандартизации документации проекта.

## Доступные шаблоны

### 📐 ADR (Architecture Decision Record)
**Файл:** `adr-template.md`

Используется для документирования архитектурных решений.

**Когда использовать:**
- Принято архитектурное решение
- Нужно зафиксировать почему выбрано конкретное решение
- Документирование trade-offs

### 📋 Спецификация функциональности
**Файл:** `feature-spec-template.md`

Используется для описания новой функциональности.

**Когда использовать:**
- Начинается новая фича
- Нужно описать требования и сценарии
- Планирование разработки

### 🔍 Code Review
**Файл:** `code-review-template.md`

Используется для стандартизации процесса code review.

**Когда использовать:**
- Проводится ревью кода
- Нужно зафиксировать замечания
- Проверка соответствия стандартам

### 🔄 Workflow
**Файл:** `workflow-template.md`

Используется для общего отслеживания прогресса задачи Project Manager-ом.

**Когда использовать:**
- Новая задача запущена
- Нужно отслеживать прохождение этапов
- Финальная сверка перед закрытием задачи

**Чем отличается от шаблонов межэтапной передачи:**
- `workflow-template` — обзорный трекинг для PM (один на задачу)
- `architecture-output`, `implementation-output` и т.д. — детальная передача результатов между агентами (по одному на этап)

### 🏗️ Architecture Output
**Файл:** `architecture-output-template.md`

Используется для передачи архитектурного решения от Architect к Developer-Mentor.
**Когда использовать:**
- Архитектор завершил проектирование
- Нужно передать ТЗ на реализацию

### 💻 Implementation Output
**Файл:** `implementation-output-template.md`

Используется для передачи результатов реализации от Developer-Mentor к QA-Specialist.

**Когда использовать:**
- Разработчик завершил реализацию
- Нужно передать код на проверку QA

### 🔍 QA Review Output
**Файл:** `qa-review-output-template.md`

Используется для передачи результатов проверки от QA-Specialist к DevOps.

**Когда использовать:**
- QA завершил проверку кода
- Нужно передать заключение для документирования

### 📖 Documentation Output
**Файл:** `documentation-output-template.md`

Используется для фиксации обновлений документации от DevOps.

**Когда использовать:**
- DevOps обновил документацию
- Нужно зафиксировать изменения

---

## Как использовать

### Шаблоны спецификаций (BA → Architect)
Скопируйте нужный шаблон в `docs/specs/`, переименуйте и заполните:

```bash
cp docs/specs/templates/adr-template.md docs/specs/adr-001-export-module.md
cp docs/specs/templates/feature-spec-template.md docs/specs/feature-user-auth.md
cp docs/specs/templates/workflow-template.md docs/specs/workflow-export-feature.md
```

### Шаблоны межэтапной передачи (Architect → Mentor → QA → DevOps)
Скопируйте нужный шаблон в `docs/specs/temp/`, переименуйте и заполните:

```bash
cp docs/specs/templates/architecture-output-template.md docs/specs/temp/architecture-login_dialog-done.md
cp docs/specs/templates/implementation-output-template.md docs/specs/temp/implementation-login_dialog-done.md
cp docs/specs/templates/qa-review-output-template.md docs/specs/temp/qa-review-login_dialog-done.md
cp docs/specs/templates/documentation-output-template.md docs/specs/temp/documentation-login_dialog-done.md
```

### Обновление статуса
По мере продвижения обновляйте статус в файле и в workflow-шаблоне.

