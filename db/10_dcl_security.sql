-- =============================================================================
-- DCL-скрипт настройки безопасности справочной БД AlphaMeterQC
-- СУБД: PostgreSQL 15+
-- Автор: В.Л. Солодюк
-- =============================================================================
-- Скрипт предназначен для настройки ролевой модели разграничения доступа
-- и включения журнала аудита изменений данных.
-- =============================================================================

SET search_path TO справочная_бд;

-- ===========================================================================
-- 1. Создание ролей доступа
-- ===========================================================================

-- Роль reader — только чтение всех таблиц схемы справочная_бд
-- Назначается всем авторизованным пользователям ПО AlphaMeterQC
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'amqc_reader') THEN
        CREATE ROLE amqc_reader;
    END IF;
END
$$;

-- Роль writer — чтение, вставка, обновление, удаление во всех таблицах
-- Назначается только уполномоченным сотрудникам
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'amqc_writer') THEN
        CREATE ROLE amqc_writer;
    END IF;
END
$$;

-- Роль admin — полный доступ к схеме, включая создание/изменение объектов
-- Назначается администраторам БД
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'amqc_admin') THEN
        CREATE ROLE amqc_admin;
    END IF;
END
$$;

-- ===========================================================================
-- 2. Назначение прав доступа к схеме
-- ===========================================================================

-- Все роли получают право использования схемы
GRANT USAGE ON SCHEMA справочная_бд TO amqc_reader, amqc_writer, amqc_admin;

-- ===========================================================================
-- 3. Права роли reader (SELECT на все таблицы)
-- ===========================================================================
GRANT SELECT ON ALL TABLES IN SCHEMA справочная_бд TO amqc_reader;

-- Права на новые таблицы, создаваемые в будущем (по умолчанию)
ALTER DEFAULT PRIVILEGES IN SCHEMA справочная_бд
    GRANT SELECT ON TABLES TO amqc_reader;

-- ===========================================================================
-- 4. Права роли writer (SELECT, INSERT, UPDATE, DELETE на все таблицы)
-- ===========================================================================
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA справочная_бд TO amqc_writer;

-- Права на последовательности (для GENERATED ALWAYS AS IDENTITY)
GRANT USAGE ON ALL SEQUENCES IN SCHEMA справочная_бд TO amqc_writer;

-- Права на новые таблицы (по умолчанию)
ALTER DEFAULT PRIVILEGES IN SCHEMA справочная_бд
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO amqc_writer;
ALTER DEFAULT PRIVILEGES IN SCHEMA справочная_бд
    GRANT USAGE ON SEQUENCES TO amqc_writer;

-- ===========================================================================
-- 5. Права роли admin (полный доступ)
-- ===========================================================================
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA справочная_бд TO amqc_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA справочная_бд TO amqc_admin;
GRANT ALL PRIVILEGES ON SCHEMA справочная_бд TO amqc_admin;

ALTER DEFAULT PRIVILEGES IN SCHEMA справочная_бд
    GRANT ALL ON TABLES TO amqc_admin;
ALTER DEFAULT PRIVILEGES IN SCHEMA справочная_бд
    GRANT ALL ON SEQUENCES TO amqc_admin;

-- ===========================================================================
-- 6. Создание пользователей и назначение ролей (пример)
-- ===========================================================================
-- В реальной среде пользователи создаются администратором БД.
-- Ниже приведены примеры для тестовой среды.

-- Пользователь для чтения (например, для АРМ инженеров)
-- CREATE USER amqc_user_reader WITH PASSWORD '***' IN ROLE amqc_reader;

-- Пользователь для записи (например, для уполномоченных сотрудников)
-- CREATE USER amqc_user_writer WITH PASSWORD '***' IN ROLE amqc_writer;

-- Пользователь-администратор
-- CREATE USER amqc_user_admin WITH PASSWORD '***' IN ROLE amqc_admin;

-- ===========================================================================
-- 7. Настройка аудита изменений данных
-- ===========================================================================

-- 7.1. Создание таблицы журнала аудита
CREATE TABLE IF NOT EXISTS ЖурналАудита (
    ИД_Записи       BIGINT        GENERATED ALWAYS AS IDENTITY
                                   PRIMARY KEY,
    ИмяПользователя VARCHAR(128)  NOT NULL,
    ВремяИзменения  TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ТипОперации     VARCHAR(10)   NOT NULL
                    CHECK (ТипОперации IN ('INSERT', 'UPDATE', 'DELETE')),
    ИмяТаблицы      VARCHAR(128)  NOT NULL,
    ИД_ЗаписиТаблицы INTEGER      NOT NULL,
    СтарыеЗначения  JSONB,
    НовыеЗначения   JSONB
);

COMMENT ON TABLE  ЖурналАудита IS 'Журнал аудита изменений данных справочной БД';
COMMENT ON COLUMN ЖурналАудита.ИД_Записи IS 'Уникальный идентификатор записи аудита';
COMMENT ON COLUMN ЖурналАудита.ИмяПользователя IS 'Имя пользователя, выполнившего операцию (current_user)';
COMMENT ON COLUMN ЖурналАудита.ВремяИзменения IS 'Время выполнения операции';
COMMENT ON COLUMN ЖурналАудита.ТипОперации IS 'Тип операции: INSERT, UPDATE, DELETE';
COMMENT ON COLUMN ЖурналАудита.ИмяТаблицы IS 'Имя изменённой таблицы';
COMMENT ON COLUMN ЖурналАудита.ИД_ЗаписиТаблицы IS 'Идентификатор изменённой записи';
COMMENT ON COLUMN ЖурналАудита.СтарыеЗначения IS 'Значения до изменения (для UPDATE и DELETE)';
COMMENT ON COLUMN ЖурналАудита.НовыеЗначения IS 'Значения после изменения (для INSERT и UPDATE)';

-- Индекс для ускорения поиска по времени и таблице
CREATE INDEX idx_аудит_время ON ЖурналАудита(ВремяИзменения);
CREATE INDEX idx_аудит_таблица ON ЖурналАудита(ИмяТаблицы);
CREATE INDEX idx_аудит_пользователь ON ЖурналАудита(ИмяПользователя);

-- Защита журнала аудита от удаления и модификации
-- Только роль amqc_admin имеет право на DELETE и UPDATE таблицы аудита
REVOKE DELETE, UPDATE ON ЖурналАудита FROM amqc_reader, amqc_writer;
GRANT SELECT ON ЖурналАудита TO amqc_reader, amqc_writer;
GRANT ALL ON ЖурналАудита TO amqc_admin;

-- 7.2. Функция аудита для триггеров
CREATE OR REPLACE FUNCTION фн_аудит_изменений()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO ЖурналАудита (ИмяПользователя, ТипОперации, ИмяТаблицы, ИД_ЗаписиТаблицы, НовыеЗначения)
        VALUES (current_user, 'INSERT', TG_TABLE_NAME, NEW.ИД_ЗаписиТаблицы, row_to_json(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO ЖурналАудита (ИмяПользователя, ТипОперации, ИмяТаблицы, ИД_ЗаписиТаблицы, СтарыеЗначения, НовыеЗначения)
        VALUES (current_user, 'UPDATE', TG_TABLE_NAME, NEW.ИД_ЗаписиТаблицы, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO ЖурналАудита (ИмяПользователя, ТипОперации, ИмяТаблицы, ИД_ЗаписиТаблицы, СтарыеЗначения)
        VALUES (current_user, 'DELETE', TG_TABLE_NAME, OLD.ИД_ЗаписиТаблицы, row_to_json(OLD));
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION фн_аудит_изменений IS 'Функция аудита для триггеров: фиксирует INSERT, UPDATE, DELETE в таблице ЖурналАудита';

-- 7.3. Создание триггеров аудита для каждой таблицы
-- Для таблицы Организация
CREATE TRIGGER trg_аудит_организация
    AFTER INSERT OR UPDATE OR DELETE ON Организация
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы СтруктурноеПодразделение
CREATE TRIGGER trg_аудит_подразделение
    AFTER INSERT OR UPDATE OR DELETE ON СтруктурноеПодразделение
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы КонтактноеЛицо
CREATE TRIGGER trg_аудит_контактноелицо
    AFTER INSERT OR UPDATE OR DELETE ON КонтактноеЛицо
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы МестоРасположения
CREATE TRIGGER trg_аудит_месторасположения
    AFTER INSERT OR UPDATE OR DELETE ON МестоРасположения
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы Объект
CREATE TRIGGER trg_аудит_объект
    AFTER INSERT OR UPDATE OR DELETE ON Объект
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы СтатусТУ
CREATE TRIGGER trg_аудит_статусту
    AFTER INSERT OR UPDATE OR DELETE ON СтатусТУ
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы ТочкаУчёта
CREATE TRIGGER trg_аудит_точкаучёта
    AFTER INSERT OR UPDATE OR DELETE ON ТочкаУчёта
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы Заявка
CREATE TRIGGER trg_аудит_заявка
    AFTER INSERT OR UPDATE OR DELETE ON Заявка
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- Для таблицы Примечание
CREATE TRIGGER trg_аудит_примечание
    AFTER INSERT OR UPDATE OR DELETE ON Примечание
    FOR EACH ROW EXECUTE FUNCTION фн_аудит_изменений();

-- ===========================================================================
-- 8. Подтверждение успешной настройки безопасности
-- ===========================================================================
DO $$
DECLARE
    cnt_roles INTEGER;
    cnt_triggers INTEGER;
BEGIN
    SELECT COUNT(*) INTO cnt_roles FROM pg_roles
        WHERE rolname IN ('amqc_reader', 'amqc_writer', 'amqc_admin');
    SELECT COUNT(*) INTO cnt_triggers FROM pg_trigger
        WHERE tgname LIKE 'trg_аудит_%';

    RAISE NOTICE 'Настройка безопасности справочной БД AlphaMeterQC завершена.';
    RAISE NOTICE '  Создано ролей: %', cnt_roles;
    RAISE NOTICE '  Создано триггеров аудита: %', cnt_triggers;
    RAISE NOTICE '  Таблица аудита: ЖурналАудита';
END;
$$;