## Распределение моделей

## 🧑‍💻 `arch-dev-qa-devOps`

*Сложный код, инфраструктура, тесты, отладка*

| Роль | Maximal | Advanced | Optimal |
|------|---------|----------|---------|
| `chat` | `Qwen3 235B` | `DeepSeek V4 Flash` | `Qwen3.6-35B` |
| `subagent` | `Qwen3 235B` | `DeepSeek V4 Flash` | `Qwen3.6-35B` |
| `edit` | `DeepSeek V4 Flash` | `Qwen3.6-35B` | `gpt-oss-20b` |
| `apply` | `DeepSeek V4 Flash` | `Qwen3.6-35B` | `gpt-oss-20b` |
| `summarize` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` |

> 🔒 **`subagent` нельзя снижать** — работает с кодом, делает рефакторинги, анализирует архитектуру.
> 💡 **Оптимальный** — лучший выбор для daily use.
> ❌ **Экономичный вариант не предусмотрен** — любое снижение качества приведёт к ошибкам в коде.

---

## 📊 `business_analyst`

*Требования, SQL, JSON, аналитика, документация*

| Роль | Maximal | Advanced | Optimal | Economical |
|------|---------|----------|---------|------------|
| `chat` | `Qwen3 235B` | `DeepSeek V4 Flash` | `Qwen3.6-35B` | `gpt-oss-20b` |
| `subagent` | `Qwen3 235B` | `DeepSeek V4 Flash` | `gpt-oss-20b` | `gpt-oss-20b` |
| `edit` | `Qwen3.6-35B` | `Qwen3.6-35B` | `gpt-oss-20b` | `Alice AI LLM Flash` |
| `apply` | `Qwen3.6-35B` | `Qwen3.6-35B` | `gpt-oss-20b` | `Alice AI LLM Flash` |
| `summarize` | `DeepSeek V4 Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` |

> ⚠️ **`subagent` в Оптимальном** — только если не генерирует сложные SQL/JSON.
> 💡 `Qwen3.6-35B` отлично справляется с JSON/SQL, `gpt-oss-20b` — базово.
> 🟢 **Экономичный** — только для простых запросов (например, суммаризация текста, простые SELECT). Для сложной аналитики используйте Оптимальный или выше.
>
> 🔐 **Ограничение для Экономичного:** `edit`/`apply` = `Alice` допустимо **только если нет работы со сложными SQL (с подзапросами, JOIN), нет генерации JSON-схем, API-дескрипторов**. Если задачи ограничиваются правкой Markdown, текста, списков — смело используйте.

---

## 📅 `project_manager`

*Планирование, коммуникации, отчёты, документация*

| Роль | Maximal | Advanced | Optimal | Economical |
|------|---------|----------|---------|------------|
| `chat` | `Qwen3 235B` | `DeepSeek V4 Flash` | `Qwen3.6-35B` | `gpt-oss-20b` |
| `subagent` | `DeepSeek V4 Flash` | `gpt-oss-20b` | `gpt-oss-20b` | `gpt-oss-20b` |
| `edit` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` |
| `apply` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` |
| `summarize` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` | `Alice AI LLM Flash` |

> ✅ **`subagent` можно безопасно снизить** — задачи простые: суммаризация, обновление статусов.
> 💡 `Alice` достаточно для правки Markdown, списков, JSON-конфигов.
> 🟢 **Экономичный** — оптимален для повседневных задач PM.
> ❌ **«Максимально эффективный» избыточен** — профиль не требует сложных операций, важнее большой контекст. Достаточно Оптимального или Экономичного.

---

## 📌 Общие правила

| Правило | Применение |
|--------|-----------|
| **`summarize`** | Везде `Alice AI LLM Flash`, кроме топ-вариантов BA (где нужна точность) → `DeepSeek V4 Flash` |
| **`edit`/`apply`** | В `dev` — не ниже `gpt-oss-20b`, в `PM` и `BA` (эконом) — можно `Alice` (только для простых задач) |
| **`chat`** | Минимум `Qwen3.6-35B` для `dev` и `BA`; для `PM` допустим `gpt-oss-20b` в экономичном |
| **`subagent`** | Не ниже `gpt-oss-20b`. В `dev` — не ниже `Qwen3.6-35B` |
| **Экономичный профиль** | Добавлен для `PM` и `BA` (только простые задачи). Для `dev` исключён — не обеспечивает стабильности |

---

## 💡 Рекомендации по выбору

| Профиль | Best choice | Reason |
|--------|-------------|--------|
| `arch-dev-qa-devOps` | **Optimal** | Высокое качество, 40–50% экономии vs топа |
| `business_analyst` | **Advanced** (или **Optimal** для экономии) | Хороший баланс: `DeepSeek` в `chat` и `subagent`, `Qwen35B` в `edit`. Для простых задач — **Economical** (с оговорками) |
| `project_manager` | **Economical** | `gpt-oss-20b` в `chat` достаточно, остальное на `Alice`. Максимальная экономия без потери качества для типовых задач |
