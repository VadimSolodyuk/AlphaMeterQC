# 🚀 Быстрый старт с Ollama в AlphaMeterQC

## ✅ Что сделано

1. ✅ **Ollama установлен** и запущен как systemd сервис
2. ✅ **Модель qwen2.5:7b загружается** (~56% завершено)
3. ✅ **Конфигурация создана** (файлы `.env` и `.env.example`)
4. ✅ **AI сервис разработан** (`src/alphameterqc/ai_service.py`)
5. ✅ **Документация написана** (`docs/ollama_setup.md`)
6. ✅ **Примеры созданы** (`examples/ollama_example.py`)

## 📦 Установленные компоненты

### Файлы конфигурации
- [`.env`](file:///home/vls/Documents/projects/AlphaMeterQC/.env) - рабочая конфигурация
- [`.env.example`](file:///home/vls/Documents/projects/AlphaMeterQC/.env.example) - шаблон для новых установок
- [`.gitignore`](file:///home/vls/Documents/projects/AlphaMeterQC/.gitignore) - исключает `.env` из Git

### Код проекта
- [`src/alphameterqc/ai_service.py`](file:///home/vls/Documents/projects/AlphaMeterQC/src/alphameterqc/ai_service.py) - основной сервис для работы с Ollama
- [`test_ollama.py`](file:///home/vls/Documents/projects/AlphaMeterQC/examples/test_ollama.py) - скрипт тестирования подключения
- [`examples/ollama_example.py`](file:///home/vls/Documents/projects/AlphaMeterQC/examples/ollama_example.py) - примеры использования

### Документация
- [`docs/ollama_setup.md`](file:///home/vls/Documents/projects/AlphaMeterQC/docs/ollama_setup.md) - полная документация по настройке

## 🎯 Как использовать

### 1. Дождаться загрузки модели

Модель [qwen2.5:7b](file:///home/vls/Documents/projects/AlphaMeterQC/.env#L13-L13) все еще загружается. Проверить статус:

```bash
ollama list
```

Когда модель появится в списке, можно продолжать.

### 2. Протестировать подключение

```bash
python3 test_ollama.py
```

Ожидаемый результат:
```
✅ Ollama API доступен!
✅ Модель 'qwen2.5:7b' доступна!
🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!
```

### 3. Запустить примеры

```bash
python3 examples/ollama_example.py
```

### 4. Интегрировать в свой код

```python
from alphameterqc.ai_service import OllamaService

# Создать сервис
service = OllamaService()

# Проверить подключение
if service.check_connection():
    # Отправить запрос
    answer = service.generate("Что такое Python?")
    print(answer)
```

## 🔧 Основные команды Ollama

```bash
# Проверить версию
ollama --version

# Список моделей
ollama list

# Скачать другую модель
ollama pull llama3.2:3b

# Запустить интерактивный чат
ollama run qwen2.5:7b

# Управление сервисом
sudo systemctl start ollama      # Запустить
sudo systemctl stop ollama       # Остановить
sudo systemctl restart ollama    # Перезапустить
sudo systemctl status ollama     # Статус
```

## 📝 Конфигурация

Все настройки в файле [`.env`](file:///home/vls/Documents/projects/AlphaMeterQC/.env):

```bash
OLLAMA_BASE_URL=http://localhost:11434
AI_MODEL=qwen2.5:7b
AI_TIMEOUT=120
AI_MAX_TOKENS=2048
AI_TEMPERATURE=0.7
```

Для смены модели:
1. Скачайте новую: `ollama pull <model_name>`
2. Измените `AI_MODEL` в `.env`
3. Перезапустите приложение

## 🐛 Решение проблем

### Ollama не отвечает
```bash
# Проверить статус сервиса
systemctl status ollama

# Посмотреть логи
journalctl -u ollama -n 50

# Перезапустить
sudo systemctl restart ollama
```

### Модель не найдена
```bash
# Проверить список моделей
ollama list

# Если пусто, дождаться завершения загрузки
# или скачать заново:
ollama pull qwen2.5:7b
```

### Медленная генерация
- Уменьшите `AI_MAX_TOKENS` в `.env`
- Используйте более легкую модель (например, `llama3.2:3b`)
- Закройте другие ресурсоемкие приложения

## 📚 Дополнительные ресурсы

- [Полная документация](docs/ollama_setup.md)
- [Примеры использования](examples/ollama_example.py)
- [Официальный сайт Ollama](https://ollama.ai)

## ✨ Следующие шаги

1. ⏳ Дождитесь завершения загрузки модели
2. 🧪 Запустите `python3 test_ollama.py`
3. 📖 Изучите примеры в `examples/ollama_example.py`
4. 🔌 Интегрируйте [`OllamaService`](file:///home/vls/Documents/projects/AlphaMeterQC/src/alphameterqc/ai_service.py) в ваш проект
5. 📝 Настройте параметры в `.env` под ваши задачи

---

**Готово!** 🎉 Теперь у вас есть полностью настроенный локальный AI-сервер для проекта AlphaMeterQC.
