# Настройка и использование Ollama с AlphaMeterQC

## 📋 Обзор

Этот документ описывает процесс установки, настройки и использования локального AI-сервера Ollama в проекте AlphaMeterQC.

## ✅ Что уже установлено

- **Ollama**: Установлен и запущен как systemd сервис
- **Модель**: [qwen2.5:7b](file:///home/vls/Documents/projects/AlphaMeterQC/.env#L13-L13) (загружается, ~46% завершено)
- **Конфигурация**: Файлы [.env](file:///home/vls/Documents/projects/AlphaMeterQC/.env) и [.env.example](file:///home/vls/Documents/projects/AlphaMeterQC/.env.example) созданы

## 🔧 Конфигурация проекта

### Переменные окружения

Все AI-настройки хранятся в файле `.env` (не коммитится в Git):

```bash
# Адрес Ollama API
OLLAMA_BASE_URL=http://localhost:11434

# Модель по умолчанию
AI_MODEL=qwen2.5:7b

# Таймаут запросов (секунды)
AI_TIMEOUT=120

# Максимальное количество токенов
AI_MAX_TOKENS=2048

# Температура генерации (0.0 - детерминировано, 1.0 - креативно)
AI_TEMPERATURE=0.7
```

### Доступные модели

Рекомендуемые модели для CPU-only режима:

| Модель | Размер | Описание |
|--------|--------|----------|
| `qwen2.5:7b` | 4.7 GB | Балансированная модель от Alibaba |
| `llama3.2:3b` | 2.0 GB | Легкая модель от Meta |
| `mistral:7b` | 4.1 GB | Эффективная модель от Mistral AI |
| `codellama:7b` | 3.8 GB | Специализирована для кода |

Для смены модели:
```bash
ollama pull <model_name>
# Обновите .env файл: AI_MODEL=<model_name>
```

## 🚀 Управление Ollama

### Проверка статуса

```bash
# Проверить версию
ollama --version

# Проверить запущенные модели
ollama list

# Проверить статус сервиса
systemctl status ollama
```

### Запуск/Остановка сервиса

```bash
# Запустить Ollama
sudo systemctl start ollama

# Остановить Ollama
sudo systemctl stop ollama

# Перезапустить
sudo systemctl restart ollama

# Автозагрузка при старте системы
sudo systemctl enable ollama
```

### Просмотр логов

```bash
# Логи сервиса
journalctl -u ollama -f

# Последние 100 строк
journalctl -u ollama -n 100
```

## 🧪 Тестирование подключения

### Использование тестового скрипта

```bash
python3 test_ollama.py
```

Скрипт проверяет:
1. Доступность Ollama API
2. Наличие указанной модели
3. Работоспособность генерации ответов

### Ручное тестирование через curl

```bash
# Проверка версии
curl http://localhost:11434/api/version

# Список моделей
curl http://localhost:11434/api/tags

# Тестовый запрос
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5:7b",
  "prompt": "Привет!",
  "stream": false
}'
```

## 💻 Интеграция с Python

### Пример использования

```python
import requests
import os
from dotenv import load_dotenv

# Загрузка конфигурации
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL = os.getenv("AI_MODEL", "qwen2.5:7b")

def ask_ai(prompt: str, max_tokens: int = 512) -> str:
    """Отправить запрос к локальной AI модели."""
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": float(os.getenv("AI_TEMPERATURE", "0.7")),
            "num_predict": max_tokens
        }
    }
    
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=int(os.getenv("AI_TIMEOUT", "120"))
    )
    
    if response.status_code == 200:
        return response.json().get("response", "")
    else:
        raise Exception(f"API error: {response.status_code}")

# Использование
answer = ask_ai("Объясни принцип SOLID")
print(answer)
```

### Установка зависимостей

```bash
pip install requests python-dotenv
```

## ⚙️ Оптимизация производительности

### Для CPU-only режима

1. **Выбор легкой модели**: Используйте модели с 3B параметрами вместо 7B+
2. **Уменьшение контекста**: Установите `AI_MAX_TOKENS=1024` или меньше
3. **Кэширование ответов**: Сохраняйте частые запросы в базу данных

### Параметры модели

В файле `.env` можно настроить:

```bash
# Более быстрая генерация (менее креативная)
AI_TEMPERATURE=0.3

# Ограничение длины ответа
AI_MAX_TOKENS=512

# Увеличенный таймаут для больших запросов
AI_TIMEOUT=180
```

## 🔍 Диагностика проблем

### Ollama не запускается

```bash
# Проверить логи
journalctl -u ollama -n 50

# Проверить порт
sudo lsof -i :11434

# Перезапустить сервис
sudo systemctl restart ollama
```

### Модель не отвечает

```bash
# Проверить загрузку модели
ollama list

# Проверить доступную память
free -h

# Убить зависшие процессы
pkill -f ollama
sudo systemctl restart ollama
```

### Медленная генерация

1. Уменьшите размер модели (используйте 3B вместо 7B)
2. Уменьшите `AI_MAX_TOKENS`
3. Закройте другие ресурсоемкие приложения

## 📚 Полезные команды Ollama

```bash
# Скачать модель
ollama pull llama3.2:3b

# Удалить модель
ollama rm qwen2.5:7b

# Запустить интерактивный чат
ollama run qwen2.5:7b

# Показать информацию о модели
ollama show qwen2.5:7b

# Создать кастомную модель с промптом
ollama create mymodel -f Modelfile
```

## 🔗 Дополнительные ресурсы

- [Официальная документация Ollama](https://ollama.ai/docs)
- [Библиотека моделей](https://ollama.ai/library)
- [GitHub репозиторий](https://github.com/ollama/ollama)

## 📝 Примечания

- Модель [qwen2.5:7b](file:///home/vls/Documents/projects/AlphaMeterQC/.env#L13-L13) требует ~4.7 GB дискового пространства
- Для работы на CPU рекомендуется минимум 8 GB RAM
- Ollama автоматически использует GPU если доступен (CUDA/Metal)
- Все запросы обрабатываются локально — данные не отправляются в интернет
