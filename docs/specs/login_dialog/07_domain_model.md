# Модель предметной сферы

**Версия:** 2.5 (итоговая)  
**Дата:** 2026-06-06  
**Автор:** Солодюк В.Л.  
**Проект:** ПО «AlphaMeterQC» / Модуль ввода данных для подключения к БД

---

## 1. Таблица классов анализа

| ID | Название | Домен | Атрибуты | Методы | Связи | Описание сущности |
|----|----------|-------|----------|--------|-------|-------------------|
| En.LOGIN.D0.01 | LoginDialog | Инициализация | - | + show() <br> + showWithDefaults(...) <br> + runAsSubprocess() | → En.LOGIN.D1.01 (зависит) <br> → En.LOGIN.D3.01 (реализует) | Главный класс модуля, предоставляющий API. Поддерживает запуск как библиотеки и как subprocess (вывод JSON в stdout). |
| En.LOGIN.D0.02 | ConnectionConfig | Инициализация | - ipAddress: string <br> - port: int <br> - username: string <br> - serviceName: string | + loadFromFile(filePath) <br> + saveAtomically(filePath) <br> + getDefaults() | → En.LOGIN.D1.01 (используется) | **Подмножество ConnectionData без пароля.** Работа с конфигурацией (хранение между сессиями). `getDefaults()` возвращает `port=1521`, `service_name="ORCL"`. Путь: `%LOCALAPPDATA%` (Windows) / `~/.config/` (Linux). |
| En.LOGIN.D1.01 | ConnectionDialog | Управление вводом и валидацией | - ipField: string <br> - portField: int <br> - usernameField: string <br> - passwordField: string <br> - serviceNameField: string <br> - okButtonEnabled: bool | + show() <br> + validateFields() <br> + highlightError(field) <br> + clearHighlight(field) <br> + enableOkButton() <br> + maskPassword() <br> + setSmartFocus() | → En.LOGIN.D0.02 (использует) <br> → En.LOGIN.D1.02 (использует) <br> → En.LOGIN.D2.01 (создаёт) <br> → En.LOGIN.D2.02 (создаёт) <br> → En.LOGIN.D3.03 (взаимодействует) | Графическое окно на базе CustomTkinter. `setSmartFocus()` переводит фокус на «Пароль», если `ip` или `username` не пустые (согласно UC.LOGIN.D0.01 Шаг 6). |
| En.LOGIN.D1.02 | Validator | Управление вводом и валидацией | - ipOrDnsPattern: regex <br> - portRange: [1,65535] <br> - usernameMaxLength: 30 <br> - serviceNamePattern: regex <br> - serviceNameOptional: bool | + validateIpOrDns(value) <br> + validatePort(port) <br> + validateUsername(username) <br> + validateServiceName(serviceName) <br> + validateAll() | → En.LOGIN.D1.01 (используется) | Проверка корректности данных. Поддерживает валидацию IPv4 и строгого DNS (strip, запрет на `-`/`.` на краях, наличие буквенно-цифрового символа — согласно SRS п. 1.6). |
| En.LOGIN.D2.01 | ConnectionData | Завершение сеанса | - ipAddress: string <br> - port: int <br> - username: string <br> - **password: string** <br> - serviceName: string | + toJson() <br> + fromJson(json) <br> + toStruct() | → En.LOGIN.D0.02 (сохраняется в: 1 → 0..1) <br> → En.LOGIN.D3.01 (передаётся) | **Полная структура данных подключения (включая пароль).** Используется только транзитно для передачи результатов вызывающей системе. **Никогда не сериализуется в файл целиком** (пароль исключается при сохранении). |
| En.LOGIN.D2.02 | CancelSignal | Завершение сеанса | - signalType: enum (CANCEL) | + getSignal() <br> + toJson() | → En.LOGIN.D3.01 (передаётся) | Сигнал отмены (F-6). В режиме subprocess сериализуется в JSON `{"status": "cancelled"}`. |
| En.LOGIN.D3.01 | IConnectionDialog | Интеграция | - | + showDialog(): ConnectionData / CancelSignal | ← En.LOGIN.D0.01 (реализует) <br> → En.LOGIN.D2.01 (возвращает) <br> → En.LOGIN.D2.02 (возвращает) | Интерфейс (API) для интеграции. Возвращает данные или сигнал отмены. |
| En.LOGIN.D3.02 | CallerSystem | Интеграция | - | + callModule() <br> + processResult(result) | → En.LOGIN.D3.01 (вызывает) | Внешняя вызывающая система (ПО «AlphaMeterQC»). |
| En.LOGIN.D3.03 | User | Интеграция | - | + enterData() <br> + confirm() <br> + cancel() | → En.LOGIN.D1.01 (взаимодействует) | Пользователь, взаимодействующий с графическим интерфейсом. |

---

## 2. Диаграмма классов (PlantUML)

``plantuml
@startuml
left to right direction
skinparam linetype ortho

' === Инициализация ===
package "Инициализация" {
    class LoginDialog {
        + show()
        + showWithDefaults(defaultIp, defaultPort, defaultUsername, defaultServiceName)
        + runAsSubprocess()
    }
    
    class ConnectionConfig {
        - ipAddress: string
        - port: int
        - username: string
        - serviceName: string
        --
        + loadFromFile(filePath)
        + saveAtomically(filePath)
        + getDefaults()
    }
}

' === Управление вводом ===
package "Управление вводом и валидацией" {
    class ConnectionDialog {
        - ipField: string
        - portField: int
        - usernameField: string
        - passwordField: string
        - serviceNameField: string
        - okButtonEnabled: bool
        --
        + show()
        + validateFields()
        + highlightError(field)
        + clearHighlight(field)
        + enableOkButton()  
        + maskPassword()
        + setSmartFocus()
    }
    
    class Validator {
        - ipOrDnsPattern: regex
        - portRange: [1,65535]
        - usernameMaxLength: 30 
        - serviceNamePattern: regex
        - serviceNameOptional: bool
        --
        + validateIpOrDns(value)
        + validatePort(port)
        + validateUsername(username)
        + validateServiceName(serviceName)
        + validateAll()
    }
}

' === Завершение сеанса ===
package "Завершение сеанса" {
    class ConnectionData {
        - ipAddress: string
        - port: int
        - username: string
        - password: string
        - serviceName: string
        --
        + toJson()
        + fromJson(json)
        + toStruct()
    }
    
    class CancelSignal {
        - signalType: enum
        --
        + getSignal()
        + toJson()
    }
}

' === Интеграция ===
package "Интеграция" {
    interface IConnectionDialog {
        + showDialog(): ConnectionData / CancelSignal
    }
    
    class CallerSystem {
        + callModule()
        + processResult(result)
    }
    
    class User {
        + enterData()
        + confirm()
        + cancel()
    }
}

' === Связи с подписями ===

' Реализация API
LoginDialog ..|> IConnectionDialog : «реализует интерфейс API»

' Создание и управление диалогом
LoginDialog --> ConnectionDialog : «создаёт и управляет\n(CustomTkinter)»

' Загрузка конфигурации
LoginDialog --> ConnectionConfig : «загружает конфигурацию\nиз файла»

' Использование валидатора
ConnectionDialog --> Validator : «использует для\nпроверки данных\n(IPv4 + строгий DNS)»

' Создание результатов
ConnectionDialog --> ConnectionData : «создаёт при\nподтверждении (F-5)»
ConnectionDialog --> CancelSignal : «создаёт при\nотмене (F-6)»

' ИСПРАВЛЕНО: ConnectionConfig использует данные из ConnectionData для сохранения
ConnectionData --> ConnectionConfig : «преобразуется в\nдля сохранения\n(без пароля)»

' Возврат результатов через API
ConnectionData ..> IConnectionDialog : «возвращается при\nуспехе (F-5)»
CancelSignal ..> IConnectionDialog : «возвращается при\nотмене (F-6)»

' Взаимодействие с внешними системами
CallerSystem --> IConnectionDialog : «вызывает API модуля\n(библиотека/subprocess)»
User --> ConnectionDialog : «взаимодействует\nчерез GUI»

@enduml
```

---

## 3. Сводка по доменам

| Домен | Сущности | Описание |
|-------|----------|----------|
| Инициализация | LoginDialog, ConnectionConfig | Загрузка конфигурации (`%LOCALAPPDATA%` / `~/.config/`), API вызова, поддержка режима subprocess |
| Управление вводом и валидацией | ConnectionDialog, Validator | Графический интерфейс (CustomTkinter), проверка данных (IPv4 + строгий DNS), умный фокус |
| Завершение сеанса | ConnectionData, CancelSignal | Результаты работы (данные/отмена), сериализация в JSON для subprocess |
| Интеграция | IConnectionDialog, CallerSystem, User | Интерфейсы и внешние акторы |

---

## 4. Сводка связей

| От | К | Тип | Кратность | Описание |
|----|---|-----|-----------|----------|
| LoginDialog | ConnectionDialog | Зависимость | 1 → 1 | LoginDialog создаёт и управляет ConnectionDialog (CustomTkinter) |
| LoginDialog | IConnectionDialog | Реализация | 1 → 1 | LoginDialog реализует интерфейс API |
| LoginDialog | ConnectionConfig | Использование | 1 → 1 | LoginDialog загружает конфигурацию |
| ConnectionDialog | Validator | Использование | 1 → 1 | ConnectionDialog использует валидатор для проверки полей (IPv4 + строгий DNS) |
| ConnectionDialog | ConnectionData | Создание | 1 → 1 | ConnectionDialog создаёт структуру данных при подтверждении (F-5) |
| ConnectionDialog | CancelSignal | Создание | 1 → 1 | ConnectionDialog создаёт сигнал отмены (F-6) |
| ConnectionConfig | ConnectionData | Сохранение | 1 → 0..1 | ConnectionConfig сохраняет данные атомарно через `os.replace` (опционально, без пароля) |
| ConnectionData | IConnectionDialog | Возврат | 1 → 1 | ConnectionData возвращается через интерфейс при успехе (F-5) |
| CancelSignal | IConnectionDialog | Возврат | 1 → 1 | CancelSignal возвращается через интерфейс при отмене (F-6) |
| CallerSystem | IConnectionDialog | Вызов | 1 → 1 | Вызывающая система использует интерфейс для вызова модуля (библиотека/subprocess) |
| User | ConnectionDialog | Взаимодействие | 1 → 1 | Пользователь взаимодействует с графическим окном |

---

## 5. Рекомендации перед началом проектирования

| № | Рекомендация | Приоритет | Ссылка на источник |
|---|--------------|-----------|---------------------|
| 1 | Реализовать `Validator` как синхронный компонент с быстрым выполнением (<0,1 с). Поддержать два regex: для IPv4 и для строгого DNS. | Обязательно | SRS п. 1.6 |
| 2 | Реализовать `ConnectionConfig.saveAtomically()` с созданием `.tmp` файла строго в той же директории и использованием `os.replace(src, dst)`. | Обязательно | ТЗ п. 4.1.5 |
| 3 | Обеспечить, чтобы пароль не логировался ни в одном методе (включая режим `debug` и `subprocess`). | Обязательно | NF-3b |
| 4 | Обеспечить неблокирующую валидацию в `ConnectionDialog`. | Обязательно | NF-2b |
| 5 | Минимизировать импорты в `LoginDialog` для быстрого старта (<0,5 с). | Рекомендуется | NF-4 |
| 6 | Реализовать метод `setSmartFocus()` в `ConnectionDialog`: если поле `ip` или `username` не пустое, фокус на «Пароль», иначе на «IP-адрес/хост». | Обязательно | UC.LOGIN.D0.01 Шаг 6 |
| 7 | Реализовать метод `runAsSubprocess()` в `LoginDialog`: при запуске из командной строки выводить результат в `stdout` в формате JSON (`{"status": "success", ...}`, `{"status": "cancelled"}` или `{"status": "error", ...}`) и завершать процесс с кодом 0 (или != 0 при ошибке). | Обязательно | UC.LOGIN.D3.01 |
| 8 | В методе `getDefaults()` класса `ConnectionConfig` явно возвращать `port=1521` и `service_name="ORCL"`. | Обязательно | F-9 |

---

## 6. Изменения по сравнению с версией 2.4

| № | Изменение | Обоснование |
|---|-----------|-------------|
| 1 | **Диаграмма классов:** Убраны избыточные стили (skinparam package, class, interface), упрощено расположение для лучшей читаемости | Улучшение визуального восприятия без потери информативности |
| 2 | **ConnectionConfig:** Добавлен комментарий «Подмножество ConnectionData без пароля» | Явное разделение ответственности для предотвращения случайного сохранения пароля |
| 3 | **ConnectionData:** Добавлен комментарий «Полная структура данных подключения (включая пароль). Никогда не сериализуется в файл целиком» | Усиление требований безопасности |
| 4 | **Рекомендации:** Заменены полные описания на краткие ссылки на ТЗ и UC | Устранение дублирования информации между артефактами |
| 5 | **Validator:** Добавлена ссылка на SRS п. 1.6 для строгой валидации DNS | Синхронизация с требованиями |
| 6 | **ConnectionDialog.setSmartFocus():** Добавлена ссылка на UC.LOGIN.D0.01 Шаг 6 | Синхронизация с вариантами использования |
```

---

### 💡 Пояснение для обучения (Почему не объединяем классы?)

Ты мог подумать: *«Зачем два класса с почти одинаковыми полями? Давайте объединим!»*

**Почему это опасно:**

1. **Принцип разделения ответственности (SRP)**: `ConnectionConfig` отвечает за **хранение настроек между сессиями**, `ConnectionData` — за **транзитную передачу результатов**. Это разные жизненные циклы.

2. **Безопасность**: Если объединить классы, разработчик может случайно вызвать `saveAtomically()` на объекте с паролем, и пароль попадёт в файл. Разделение классов делает это **физически невозможным** — у `ConnectionConfig` просто нет атрибута `password`.

3. **Разные методы**: У `ConnectionConfig` есть `loadFromFile()`/`saveAtomically()`, у `ConnectionData` — `toJson()`/`fromJson()`. Объединение создаст "божественный объект" с кучей методов, которые не всегда имеют смысл вместе.

**Компромисс в коде**: При реализации можно использовать `dataclass` с общим базовым классом:
```
from dataclasses import dataclass

@dataclass
class ConnectionBase:
    ip: str
    port: int
    username: str
    service_name: str

@dataclass
class ConnectionConfig(ConnectionBase):
    # Методы для работы с файлом
    def loadFromFile(self, filePath): ...
    def saveAtomically(self, filePath): ...

@dataclass  
class ConnectionData(ConnectionBase):
    password: str  # Единственное отличие
    # Методы для сериализации
    def toJson(self): ...
```

Это даёт **переиспользование кода** (DRY) без нарушения **разделения ответственности** (SRP).

---

**Готово!** Теперь база документации полностью синхронизирована и готова к переходу к коду. Напиши **"Переходим к структуре и коду"**, и мы начнём с Шага 1 (структура проекта) и Шага 2 (класс `Validator` с тестами).