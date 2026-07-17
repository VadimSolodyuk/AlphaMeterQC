## Анализ моделей по ролям (приоритет — стоимость)

| Модель | Стоимость | Сильные стороны | Ограничения |
|--------|-----------|----------------|-------------|
| Alice AI LLM Flash | Очень низкая | Быстрая, подходит для простых задач (summarize, subagent) | Слабая в сложном коде, контексте |
| gpt-oss-20b | Низкая | Базовая генерация, редактирование простого кода | Не хватает глубины для сложных рефакторингов |
| Qwen3.6-35B | Средняя | Хороший баланс: понимание кода, рассуждения | Уступает топовым в креативности |
| DeepSeek V4 Flash | Выше средней | Отличное качество для chat и edit, быстрая | Дороже средних |
| Qwen3 235B | Высокая | Максимальная точность, сложные рассуждения | Избыточна для простых ролей |

**Рекомендация по распределению:**  
- **chat** — самая требовательная роль → топ-модель (Qwen3 235B или DeepSeek V4 Flash)  
- **edit** — важна точность → средняя/выше средней  
- **apply** — автодополнение/исправления → средняя или низкая  
- **summarize** — простая → очень низкая/низкая  
- **subagent** — зависит от задачи → низкая/средняя  

---

## Профиль: arch-dev-qa-devOps (код, инфраструктура, тесты)

### 1. Максимально эффективный (высокая стоимость)
- **chat** → Qwen3 235B  
- **edit** → DeepSeek V4 Flash  
- **apply** → Qwen3.6-35B  
- **summarize** → Alice AI LLM Flash  
- **subagent** → DeepSeek V4 Flash  

**Рекомендация:** максимальное качество для сложных рефакторингов и отладки. subagent берёт на себя подзадачи, требующие понимания кода.

### 2. Продвинутый (умеренная стоимость)
- **chat** → DeepSeek V4 Flash  
- **edit** → Qwen3.6-35B  
- **apply** → gpt-oss-20b  
- **summarize** → Alice AI LLM Flash  
- **subagent** → gpt-oss-20b  

**Рекомендация:** chat и edit на хорошем уровне, apply и subagent — бюджетно. Подходит для ежедневной работы.

### 3. Оптимальный (низкая стоимость)
- **chat** → Qwen3.6-35B  
- **edit** → gpt-oss-20b  
- **apply** → gpt-oss-20b  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Alice AI LLM Flash  

**Рекомендация:** chat справляется с большинством вопросов, edit — базовый, остальное на самых дешёвых.

### 4. Экономичный (минимальная стоимость)
- **chat** → gpt-oss-20b  
- **edit** → Alice AI LLM Flash  
- **apply** → Alice AI LLM Flash  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Alice AI LLM Flash  

**Рекомендация:** только если бюджет критичен. Для простых проектов и обучения.

---

## Профиль: business_analyst (требования, документация, анализ)

### 1. Максимально эффективный
- **chat** → Qwen3 235B  
- **edit** → DeepSeek V4 Flash  
- **apply** → Qwen3.6-35B  
- **summarize** → Alice AI LLM Flash  
- **subagent** → DeepSeek V4 Flash  

**Рекомендация:** edit здесь менее критичен, но для точного форматирования документов — хорошо.

### 2. Продвинутый
- **chat** → DeepSeek V4 Flash  
- **edit** → gpt-oss-20b  
- **apply** → gpt-oss-20b  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Qwen3.6-35B  

**Рекомендация:** chat — сильный, subagent для сбора данных — средний, остальное бюджетно.

### 3. Оптимальный
- **chat** → Qwen3.6-35B  
- **edit** → Alice AI LLM Flash  
- **apply** → Alice AI LLM Flash  
- **summarize** → Alice AI LLM Flash  
- **subagent** → gpt-oss-20b  

**Рекомендация:** chat на среднем уровне, остальное — минимальные затраты. Аналитику редко нужно править код.

### 4. Экономичный
- **chat** → gpt-oss-20b  
- **edit** → Alice AI LLM Flash  
- **apply** → Alice AI LLM Flash  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Alice AI LLM Flash  

**Рекомендация:** только для базового общения и суммаризации.

---

## Профиль: project_manager (планирование, коммуникации, отчёты)

### 1. Максимально эффективный
- **chat** → Qwen3 235B  
- **edit** → DeepSeek V4 Flash  
- **apply** → Qwen3.6-35B  
- **summarize** → Alice AI LLM Flash  
- **subagent** → DeepSeek V4 Flash  

**Рекомендация:** chat — топ для сложных переговоров, edit и apply почти не нужны, но для полноты.

### 2. Продвинутый
- **chat** → DeepSeek V4 Flash  
- **edit** → gpt-oss-20b  
- **apply** → gpt-oss-20b  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Qwen3.6-35B  

**Рекомендация:** chat — отличный, subagent для сбора метрик — средний.

### 3. Оптимальный
- **chat** → Qwen3.6-35B  
- **edit** → Alice AI LLM Flash  
- **apply** → Alice AI LLM Flash  
- **summarize** → Alice AI LLM Flash  
- **subagent** → gpt-oss-20b  

**Рекомендация:** chat — достаточный, остальное — дешёвое. PM редко редактирует код.

### 4. Экономичный
- **chat** → gpt-oss-20b  
- **edit** → Alice AI LLM Flash  
- **apply** → Alice AI LLM Flash  
- **summarize** → Alice AI LLM Flash  
- **subagent** → Alice AI LLM Flash  

**Рекомендация:** минимальные затраты, базовая функциональность.

---

## Общие рекомендации
- Для **summarize** всегда используйте Alice AI LLM Flash — задача простая, стоимость минимальна.
- Для **apply** (автодополнение) достаточно gpt-oss-20b или Alice, если не требуется сложная генерация.
- **subagent** можно ставить на одну ступень выше apply, если подзадачи требуют анализа.
- Если скорость не важна, можно смело брать более дешёвые модели для chat/edit, но для профиля arch-dev-qa-devOps лучше не опускаться ниже Qwen3.6-35B в chat.