## Распределение моделей


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

## Форма коментариев:

contextLength: 65536 # 32768 | 65536 | 131072 (65536 — макс. контекст для глубокого анализа требований)
maxTokens: 4096 # 2048 | 4096 (4096 — для развёрнутых ответов BA)
temperature: 0.3 # 0.3 — баланс точности и креативности для анализа требований
maxPromptTokens: 500 # 300 | 800 (500 — баланс между объёмом контекста и скоростью обработки)
prefixPercentage: 0.6 # 0.5 | 0.8 (0.6 — больше внимания префиксу, помогает точнее продолжить существующий код)
maxSuffixPercentage: 0.2 # 0.1 | 0.3 (0.3 — достаточно суффикса для осмысленного продолжения, не перегружает модель)