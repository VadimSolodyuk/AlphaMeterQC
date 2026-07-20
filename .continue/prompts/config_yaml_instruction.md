---
name: generate-documentation
description: 
invokable: true
---

# Шпаргалка по config.yaml для Continue (с пояснениями неявных параметров)

Добавляю комментарии `#` к полям, которые требуют контекста — что они значат, когда и зачем их использовать.

## Обязательные поля верхнего уровня
```yaml
name: "Мой проект"          # отображаемое имя конфигурации
version: "1.0.0"            # версия конфига (semver) — для совместимости
```

## metadata
```yaml
metadata:
  tags: "ai, coding"              # теги для поиска/фильтрации в UI
  sourceCodeUrl: "https://..."    # ссылка на репозиторий
  description: "Описание"         # краткое описание
  author: "Имя"                   # автор конфига
  license: "MIT"                  # лицензия
  iconUrl: "https://..."          # иконка для отображения
```

## env (глобальные переменные окружения)
```yaml
env:
  MY_VAR: "value"          # переменные, которые будут доступны всем моделям и провайдерам
  COUNT: 42                # можно переопределить на уровне модели
  DEBUG: true
```
Типы: string, number, boolean.

## requestOptions (глобальные настройки HTTP)
```yaml
requestOptions:
  timeout: 30000                    # таймаут запроса в мс (по умолчанию может быть 60000)
  verifySsl: true                   # проверять SSL-сертификаты (отключать только для dev)
  caBundlePath: "/path/to/ca.pem"   # кастомный CA-сертификат (строка или массив)
  proxy: "http://proxy:8080"        # HTTP-прокси для всех запросов
  headers:                          # кастомные заголовки, добавляемые к каждому запросу
    Authorization: "Bearer xxx"
  extraBodyProperties:               # дополнительные поля в теле запроса (например, для кастомных API)
    customField: "value"
  noProxy: ["localhost", "127.0.0.1"]  # адреса, исключённые из прокси
  clientCertificate:                  # клиентский сертификат для mTLS
    cert: "/path/to/cert.pem"
    key: "/path/to/key.pem"
    passphrase: "secret"              # опционально
```

## models (массив моделей)

### Прямое описание
```yaml
models:
  - name: "my-model"                  # уникальное имя в рамках конфига
    model: "gpt-4o"                   # идентификатор модели у провайдера
    provider: "openai"                # провайдер (например openai, anthropic, ollama)
    apiKey: "sk-..."                  # ключ API (можно использовать ${ENV_VAR})
    apiBase: "https://..."            # кастомный endpoint (для прокси или self-hosted)
    contextLength: 128000             # максимальный контекст модели (токены)
    roles: ["chat", "edit"]           # для каких задач использовать модель (см. enum)
    capabilities: ["tool_use", "image_input"]  # возможности модели (влияет на выбор Continue)
    defaultCompletionOptions:
      maxTokens: 4096                 # макс. токенов в ответе
      temperature: 0.7                # креативность (0-2)
      topP: 0.9                       # nucleus sampling
      topK: 40                        # top-k sampling
      minP: 0.05                      # минимальная вероятность токена
      presencePenalty: 0.0            # штраф за повтор тем
      frequencyPenalty: 0.0           # штраф за частые токены
      stop: ["\n\n"]                  # стоп-слова (массив строк)
      n: 1                            # количество генераций
      reasoning: true                 # включить reasoning (для o1, claude-sonnet)
      reasoningBudgetTokens: 2000     # бюджет токенов на reasoning
      promptCaching: true             # кеширование промпта (экономия токенов)
      stream: true                    # стриминг ответа
      keepAlive: 30                   # время удержания модели в памяти (сек, для ollama)
    cacheBehavior:                    # управление кешированием контекста
      cacheSystemMessage: true        # кешировать системное сообщение (экономия)
      cacheConversation: false        # кешировать историю диалога (осторожно: утечка памяти)
    requestOptions:                   # переопределение глобальных requestOptions для этой модели
      timeout: 60000
    embedOptions:                     # настройки эмбеддингов (для роли embed)
      maxChunkSize: 512               # макс. размер чанка в токенах
      maxBatchSize: 16                # макс. батч для эмбеддингов
      embeddingPrefixes:              # префиксы для разных типов запросов (query/document)
        query: "search_query: "
        document: "search_document: "
    chatOptions:                      # настройки чата (для роли chat)
      baseSystemMessage: "Ты — помощник"  # системное сообщение по умолчанию
      baseAgentSystemMessage: "..."       # системное сообщение для агента
      basePlanSystemMessage: "..."        # системное сообщение для планирования
      toolOverrides:                     # переопределение описаний инструментов
        my_tool:
          description: "Описание"        # новое описание для модели
          displayTitle: "Мой инструмент"
          wouldLikeTo: "хочет"
          isCurrently: "сейчас"
          hasAlready: "уже"
          systemMessageDescription:      # описание для системного сообщения
            prefix: "Используй инструмент"
            exampleArgs: [["arg1", "value1"], ["arg2", 42]]
          disabled: false                # отключить инструмент для этой модели
    promptTemplates:                    # шаблоны промптов для разных ролей
      chat: "chatml"                    # один из enum (см. ниже)
      apply: "custom_apply_template"    # кастомный шаблон (строка)
      edit: "custom_edit_template"
      autocomplete: "custom_ac_template"
    autocompleteOptions:                # настройки автодополнения (для роли autocomplete)
      disable: false                    # отключить автодополнение для этой модели
      maxPromptTokens: 256              # макс. токенов в промпте автодополнения
      debounceDelay: 300                # задержка перед запросом (мс)
      modelTimeout: 5000                # таймаут модели (мс)
      maxSuffixPercentage: 0.3          # макс. доля суффикса от всего предсказания
      prefixPercentage: 0.5             # доля префикса в промпте
      transform: true                   # применять трансформацию кода
      template: "{{prefix}}<FILL>{{suffix}}"  # шаблон для infill
      onlyMyCode: true                  # учитывать только код пользователя
      useCache: true                    # кешировать результаты
      useImports: true                  # учитывать импорты
      useRecentlyEdited: true           # учитывать недавно отредактированные файлы
      useRecentlyOpened: true           # учитывать недавно открытые файлы
      experimental_includeClipboard: false  # включать буфер обмена (экспериментально)
      experimental_includeRecentlyVisitedRanges: false
      experimental_includeRecentlyEditedRanges: false
      experimental_includeDiff: false
      experimental_enableStaticContextualization: false
    useLegacyCompletionsEndpoint: false  # использовать старый endpoint completions (не chat)
    useResponsesApi: false               # использовать Responses API (OpenAI)
    env:                                 # переменные окружения только для этой модели
      MODEL_VAR: "value"
```

### Ссылка на предопределённую модель (uses)
```yaml
models:
  - uses: "anthropic/claude-sonnet-4-6"   # идентификатор из списка известных моделей
    with:                                 # параметры, подставляемые в шаблон
      apiKey: "sk-..."                    # обычно apiKey, apiBase, model
    override:                             # переопределение любых полей (как в прямом описании)
      name: "my-claude"
      contextLength: 200000
      defaultCompletionOptions:
        temperature: 0.5
```
**Контекст:** `uses` позволяет не дублировать полную конфигурацию популярных моделей. Список известных идентификаторов в схеме (например `anthropic/claude-sonnet-4-6`, `openai/gpt-4o`, `ollama/deepseek-r1` и др.).  
`with` — параметры, которые шаблон ожидает (обычно apiKey, apiBase).  
`override` — любые поля из прямого описания, заменяющие значения по умолчанию.

## context (провайдеры контекста)
```yaml
context:
  - provider: "file"              # встроенный провайдер (например file, codebase, diff)
    params:                       # параметры зависят от провайдера
      path: "./src"
  - uses: "continue-ai/codebase"  # ссылка на предопределённый провайдер
    with:
      apiKey: "..."
    override:
      name: "my-codebase"
      params:
        maxResults: 10
```
**Контекст:** провайдеры контекста определяют, какую информацию Continue будет автоматически подгружать в промпт (файлы, результаты поиска, diff и т.д.).

## data (источники данных)
```yaml
data:
  - name: "my-db"                 # уникальное имя источника
    destination: "sqlite:///data.db"  # строка подключения (зависит от типа)
    schema: "1.0.0"               # версия схемы (semver) — для миграций
    level: "all"                  # уровень доступа: "all" (весь код) или "noCode" (только метаданные)
    events: ["fileChange"]        # события, при которых данные обновляются (например fileChange, timer)
    requestOptions: {...}         # настройки HTTP для этого источника
    apiKey: "..."                 # ключ API для источника
  - uses: "continue-ai/postgres"  # ссылка на предопределённый источник
    with:
      connectionString: "..."
    override:
      name: "pg"
      schema: "2.0.0"
```
**Контекст:** `data` — это внешние источники данных (БД, API), к которым Continue может обращаться.  
`level: "noCode"` — если источник содержит чувствительные данные, не связанные с кодом.  
`events` — триггеры для обновления данных (например при изменении файла).

## mcpServers (MCP-серверы)

### stdio (локальный процесс)
```yaml
mcpServers:
  - name: "my-server"             # уникальное имя
    command: "npx"                # исполняемый файл
    args: ["-y", "@modelcontextprotocol/server-filesystem", "./"]
    env:                          # переменные окружения для процесса
      NODE_ENV: "production"
    cwd: "/project"               # рабочая директория
    connectionTimeout: 30         # таймаут подключения (сек, >0)
    # неявные поля:
    serverName: "filesystem"      # имя сервера (для логирования)
    faviconUrl: "https://..."     # иконка в UI
    sourceFile: ".continue/mcp/my-server.json"  # файл, откуда загружена конфигурация
    sourceSlug: "my-server"       # slug для ссылок
```

### sse / streamable-http (удалённый сервер)
```yaml
  - name: "remote-server"
    url: "https://example.com/sse"
    type: "sse"                   # или "streamable-http" (разные протоколы)
    apiKey: "sk-..."              # ключ для аутентификации
    requestOptions: {...}         # настройки HTTP для подключения
```

### Ссылка на предопределённый
```yaml
  - uses: "continue-ai/mcp-filesystem"
    with:
      rootDir: "/project"
    override:
      name: "fs"
      command: "npx"
```
**Контекст:** MCP-серверы предоставляют инструменты (инструменты MCP).  
`type: "sse"` — Server-Sent Events (односторонний поток).  
`type: "streamable-http"` — двусторонний HTTP-стриминг.  
`connectionTimeout` — время ожидания первого сообщения от сервера.

## rules (правила)
```yaml
rules:
  - "Всегда используй английские имена переменных"  # простое текстовое правило
  - name: "no-console-log"          # уникальное имя правила
    rule: "Не используй console.log в production"  # текст правила
    description: "Заменяй на логгер"  # описание для UI
    globs: ["src/**/*.ts"]          # файлы, к которым применяется (glob)
    regex: ["console\\.log"]        # регулярные выражения для поиска нарушений
    alwaysApply: true               # применять всегда (даже если не запрошено)
    invokable: false                # можно ли вызвать правило командой (например /rule)
    sourceFile: ".continue/rules/no-console.md"  # файл с правилом (альтернатива полю rule)
  - uses: "continue-ai/eslint"      # ссылка на предопределённое правило
    with:
      config: ".eslintrc.json"
```
**Контекст:** правила — это инструкции для модели, как вести себя в проекте.  
`alwaysApply: true` — правило будет добавлено в системное сообщение каждого запроса.  
`invokable: true` — правило можно вызвать вручную через `/rule no-console-log`.  
`globs` и `regex` — фильтры для автоматического применения к определённым файлам.

## prompts (шаблоны промптов)
```yaml
prompts:
  - name: "review"                  # уникальное имя
    description: "Код-ревью"        # описание для UI
    prompt: "Проверь код на ошибки: {{code}}"  # шаблон с переменными
    sourceFile: ".continue/prompts/review.md"  # файл с промптом (альтернатива полю prompt)
  - uses: "continue-ai/explain"     # ссылка на предопределённый промпт
    with:
      language: "python"
    override:
      name: "explain-py"
      prompt: "Объясни код на Python: {{code}}"
```
**Контекст:** промпты — это готовые шаблоны для быстрых действий (например `/review`, `/explain`).  
Переменные в шаблоне (например `{{code}}`) подставляются автоматически.

## docs (документация для поиска)
```yaml
docs:
  - name: "React"                   # название документации
    startUrl: "https://react.dev"   # начальная страница для краулинга
    rootUrl: "https://react.dev"    # корневой URL (ограничивает краулинг)

