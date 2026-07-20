---
name: informations
description: Информация по Continue
alwaysApply: false
invokable: false
---


Если `generate_docs` отображается как именованный промпт в интерфейсе Continue, а `assistant` и `context_transfer` — **не подсвечиваются и не распознаются**, возможны следующие причины:

---

### 1. **Расширение файла: `.md` vs `.prompt`**
Continue **по умолчанию** может сканировать только файлы с расширением `.prompt` в папке `.continue/prompts/`.

> ❌ `.continue/prompts/assistant.md` — **не будет загружен**
>
> ✅ `.continue/prompts/assistant.prompt` — **будет распознан**

🔹 **Решение**:  
Переименуй файлы:
```bash
mv .continue/prompts/assistant.md        .continue/prompts/assistant.prompt
mv .continue/prompts/context_transfer.md .continue/prompts/context_transfer.prompt
mv .continue/prompts/generate_docs.md    .continue/prompts/generate_docs.prompt
```

> 💡 Даже если `generate_docs.md` сейчас работает — это может быть из-за кэша или ручного вызова. Для стабильной работы используй `.prompt`.

---

### 2. **Кодировка или символы в начале файла**
Иногда в `.md`-файлах редакторы добавляют **BOM (Byte Order Mark)** или пробелы перед `---`, что ломает парсинг YAML.

🔹 **Проверь**:
- Файл должен начинаться **ровно с** `---` (без пробелов, табов, невидимых символов).
- Кодировка — **UTF-8 без BOM**.

---

### 3. **Поле `invokable: true` — обязательно для отображения в списке**
Ты его указал — хорошо. Но если есть синтаксическая ошибка в YAML (например, отступы), парсер может проигнорировать файл.

🔹 Проверь валидность YAML:
```yaml
---
name: Assistant
description: Асистент по разработке ПО
invokable: true
---
```
→ всё верно, **но только если нет ошибок в отступах или символах**.

---

### ✅ Что делать:
1. **Переименуй `.md` → `.prompt`**
2. Убедись, что файл начинается **ровно с** `---`, без пробелов
3. Перезапусти Continue или обнови промпты (через команду `Continue: Reload Configuration`)

---

После этого все три промпта должны отображаться как именованные.