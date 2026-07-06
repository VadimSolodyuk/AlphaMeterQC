# Инструкция по развёртыванию и эксплуатации справочной БД AlphaMeterQC

**Автор:** В.Л. Солодюк
**Проект:** ПО «AlphaMeterQC» / Модуль справочной БД
**СУБД:** PostgreSQL 15+

---

## 1. Требования к окружению

### 1.1. Аппаратные требования

| Параметр | Минимальные | Рекомендуемые |
|:---------|:------------|:--------------|
| Процессор | 2 ядра, 2 ГГц | 4 ядра, 3 ГГц |
| ОЗУ | 2 ГБ | 8 ГБ |
| Дисковое пространство | 10 ГБ | 50 ГБ (SSD) |
| Сеть | 100 Мбит/с | 1 Гбит/с |

### 1.2. Программные требования

| Компонент | Версия | Назначение |
|:----------|:-------|:-----------|
| ОС | Linux (Ubuntu 22.04+/Debian 12+) или Windows Server 2019+ | Серверная ОС |
| PostgreSQL | 15.x или выше | Система управления базами данных |
| psql | 15.x или выше | Клиент командной строки PostgreSQL |
| OpenSSL | 1.1.1+ | Защита соединений (TLS/SSL) |

---

## 2. Порядок развёртывания

### 2.1. Установка PostgreSQL

**Linux (Ubuntu/Debian):**

```bash
# Установка PostgreSQL 15
sudo apt update
sudo apt install -y postgresql-15 postgresql-client-15

# Проверка статуса
sudo systemctl status postgresql

# Включение автозапуска
sudo systemctl enable postgresql
```

**Windows Server:**

1. Скачать дистрибутив PostgreSQL 15 с официального сайта https://www.postgresql.org/download/
2. Запустить установщик, следовать инструкциям мастера установки
3. Задать пароль для суперпользователя `postgres`
4. Оставить порт по умолчанию `5432`

### 2.2. Настройка локали и кодировки

Для корректной работы с русскоязычными данными необходимо создать базу данных с поддержкой UTF-8 и русской локали:

```bash
# Подключение к серверу PostgreSQL
sudo -u postgres psql
```

```sql
-- Проверка доступных локалей
SELECT datname, datcollate, datctype FROM pg_database;

-- Создание базы данных с русской локалью
CREATE DATABASE alphameterqc
    WITH ENCODING 'UTF8'
         LC_COLLATE 'ru_RU.UTF-8'
         LC_CTYPE 'ru_RU.UTF-8'
         TEMPLATE template0;

-- Подключение к созданной БД
\c alphameterqc;
```

### 2.3. Выполнение DDL-скрипта создания схемы

```bash
# Выполнение DDL-скрипта
psql -h localhost -U postgres -d alphameterqc -f docs/specs/db/08_ddl_schema.sql
```

**Ожидаемый результат:** скрипт создаст схему `справочная_бд`, 9 таблиц, 10 индексов, ограничения целостности и выведет подтверждение:

```
NOTICE:  Схема справочной БД AlphaMeterQC успешно создана.
NOTICE:  Создано таблиц: 9
NOTICE:  Создано индексов: 10
NOTICE:  Создано ограничений UNIQUE: 3
NOTICE:  Создано ограничений CHECK: 1
```

### 2.4. Выполнение DML-скрипта начального наполнения

```bash
# Выполнение DML-скрипта
psql -h localhost -U postgres -d alphameterqc -f docs/specs/db/09_dml_seed.sql
```

**Ожидаемый результат:** скрипт наполнит таблицы демонстрационными данными и выведет подтверждение:

```
NOTICE:  Наполнение справочной БД AlphaMeterQC завершено.
NOTICE:   Организации:                10
NOTICE:   Структурные подразделения:  10
NOTICE:   Контактные лица:            10
NOTICE:   Места расположения:         10
NOTICE:   Объекты:                    10
NOTICE:   Точки учёта:                10
NOTICE:   Статусы ТУ:                 6
NOTICE:   Заявки:                     10
NOTICE:   Примечания:                 10
```

### 2.5. Выполнение DCL-скрипта настройки безопасности

```bash
# Выполнение DCL-скрипта
psql -h localhost -U postgres -d alphameterqc -f docs/specs/db/10_dcl_security.sql
```

**Ожидаемый результат:** скрипт создаст роли `amqc_reader`, `amqc_writer`, `amqc_admin`, настроит права доступа, создаст таблицу аудита `ЖурналАудита` и триггеры аудита для всех 9 таблиц.

### 2.6. Проверка корректности развёртывания

```bash
# Подключение к БД
psql -h localhost -U postgres -d alphameterqc

# Проверка списка таблиц
\dt справочная_бд.*

# Проверка количества записей
SELECT 'Организация' AS Таблица, COUNT(*) AS Записей FROM справочная_бд.Организация
UNION ALL
SELECT 'СтруктурноеПодразделение', COUNT(*) FROM справочная_бд.СтруктурноеПодразделение
UNION ALL
SELECT 'КонтактноеЛицо', COUNT(*) FROM справочная_бд.КонтактноеЛицо
UNION ALL
SELECT 'МестоРасположения', COUNT(*) FROM справочная_бд.МестоРасположения
UNION ALL
SELECT 'Объект', COUNT(*) FROM справочная_бд.Объект
UNION ALL
SELECT 'СтатусТУ', COUNT(*) FROM справочная_бд.СтатусТУ
UNION ALL
SELECT 'ТочкаУчёта', COUNT(*) FROM справочная_бд.ТочкаУчёта
UNION ALL
SELECT 'Заявка', COUNT(*) FROM справочная_бд.Заявка
UNION ALL
SELECT 'Примечание', COUNT(*) FROM справочная_бд.Примечание;

# Проверка ссылочной целостности (пример)
SELECT COUNT(*) AS Нарушения_ссылочной_целостности
FROM справочная_бд.ТочкаУчёта tu
LEFT JOIN справочная_бд.Объект o ON tu.ИД_Объекта = o.ИД_Объекта
WHERE o.ИД_Объекта IS NULL;
```

---

## 3. Настройка подключения

### 3.1. Настройка pg_hba.conf

Для обеспечения доступа с АРМ инженеров по локальной сети необходимо настроить файл `pg_hba.conf`:

```bash
# Расположение файла (Linux)
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Добавить строки для аутентификации пользователей:

```
# Разрешить подключение с локальной сети (192.168.x.x) по паролю
host    alphameterqc    amqc_reader     192.168.0.0/16    scram-sha-256
host    alphameterqc    amqc_writer     192.168.0.0/16    scram-sha-256
host    alphameterqc    amqc_admin      127.0.0.1/32      scram-sha-256
```

### 3.2. Настройка postgresql.conf

```bash
sudo nano /etc/postgresql/15/main/postgresql.conf
```

Рекомендуемые параметры:

```
# Слушать все сетевые интерфейсы
listen_addresses = '*'

# Параметры производительности (для сервера с 8 ГБ ОЗУ)
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB
maintenance_work_mem = 512MB

# Параметры подключения
max_connections = 50
```

### 3.3. Перезапуск PostgreSQL

```bash
sudo systemctl restart postgresql
```

### 3.4. Строка подключения для ПО AlphaMeterQC

```
postgresql://amqc_reader:password@192.168.1.100:5432/alphameterqc
```

---

## 4. Резервное копирование и восстановление

### 4.1. Полное резервное копирование

```bash
# Создание полной резервной копии
pg_dump -h localhost -U postgres -d alphameterqc \
    --format=custom \
    --file=/backup/alphameterqc_$(date +%Y%m%d_%H%M%S).dump \
    --verbose
```

### 4.2. Восстановление из резервной копии

```bash
# Восстановление базы данных
pg_restore -h localhost -U postgres -d alphameterqc \
    --clean \
    --if-exists \
    --verbose \
    /backup/alphameterqc_20260504_120000.dump
```

### 4.3. Регламент резервного копирования

| Тип копирования | Периодичность | Время выполнения | Срок хранения |
|:----------------|:--------------|:-----------------|:--------------|
| Полная | Ежедневно | 02:00 | 30 дней |
| Инкрементальная (WAL) | Непрерывно | — | 7 дней |

---

## 5. Мониторинг и обслуживание

### 5.1. Проверка активности подключений

```sql
SELECT pid, usename, application_name, client_addr, state
FROM pg_stat_activity
WHERE datname = 'alphameterqc';
```

### 5.2. Анализ размера таблиц

```sql
SELECT
    relname AS Таблица,
    pg_size_pretty(pg_total_relation_size(relid)) AS Общий_размер,
    pg_size_pretty(pg_relation_size(relid)) AS Размер_данных,
    pg_size_pretty(pg_indexes_size(relid)) AS Размер_индексов
FROM pg_catalog.pg_statio_user_tables
WHERE schemaname = 'справочная_бд'
ORDER BY pg_total_relation_size(relid) DESC;
```

### 5.3. Обновление статистики

```sql
ANALYZE справочная_бд.Организация;
ANALYZE справочная_бд.ТочкаУчёта;
-- ... для всех таблиц
```

Или для всех таблиц схемы:

```sql
ANALYZE справочная_бд.*;
```

---

## 6. Устранение неполадок

### 6.1. Не удаётся подключиться к БД

1. Проверить, запущен ли PostgreSQL:
   ```bash
   sudo systemctl status postgresql
   ```

2. Проверить настройки pg_hba.conf:
   ```bash
   sudo cat /etc/postgresql/15/main/pg_hba.conf | grep alphameterqc
   ```

3. Проверить, слушает ли сервер нужный порт:
   ```bash
   sudo ss -tlnp | grep 5432
   ```

### 6.2. Ошибка «relation does not exist»

Убедиться, что установлен `search_path`:

```sql
SET search_path TO справочная_бд;
```

Или использовать полное имя таблицы:

```sql
SELECT * FROM справочная_бд.Организация;
```

### 6.3. Ошибка нарушения внешнего ключа при вставке

Проверить, что ссылочные значения существуют в родительской таблице:

```sql
-- Пример: проверка существования объекта перед вставкой ТУ
SELECT ИД_Объекта FROM справочная_бд.Объект WHERE ИД_Объекта = 1;
```

---

## 7. Контрольный список развёртывания

| № | Действие | Выполнено |
|:-:|:---------|:---------:|
| 1 | Установлен PostgreSQL 15+ | ☐ |
| 2 | Создана БД `alphameterqc` с локалью `ru_RU.UTF-8` | ☐ |
| 3 | Выполнен DDL-скрипт (08_ddl_schema.sql) | ☐ |
| 4 | Выполнен DML-скрипт (09_dml_seed.sql) | ☐ |
| 5 | Выполнен DCL-скрипт (10_dcl_security.sql) | ☐ |
| 6 | Настроен pg_hba.conf для доступа по локальной сети | ☐ |
| 7 | Настроен postgresql.conf (shared_buffers, max_connections) | ☐ |
| 8 | Выполнен перезапуск PostgreSQL | ☐ |
| 9 | Проверено подключение с АРМ инженера | ☐ |
| 10 | Настроено резервное копирование | ☐ |
| 11 | Созданы пользователи БД и назначены роли | ☐ |
| 12 | Проверена работа триггеров аудита | ☐ |