"""
Модульные тесты для классов Validator и ConnectionConfig.

Покрывает требования:
- F-2: Валидация в реальном времени (IPv4 + строгий DNS)
- F-7: Атомарное сохранение через os.replace
- F-8, F-9, F-13: Загрузка/сохранение конфигурации

Согласно спецификации:
- 04_srs.md (v2.9), раздел 1.6
- 08_technical_specification.md (v2.9), п. 4.1.2 (граничные значения)
"""

import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

from alphameterqc.login_dialog.model import ConnectionConfig, Validator

# ============================================================================
# Тесты для Validator.validate_ip_or_dns
# ============================================================================


class TestValidateIpOrDns:
    """Тесты валидации IP-адреса и DNS-имени."""

    # === Валидные IPv4 ===

    @pytest.mark.parametrize(
        "ip",
        [
            "0.0.0.0",
            "127.0.0.1",
            "192.168.1.1",
            "255.255.255.255",
            "10.0.0.1",
        ],
    )
    def test_valid_ipv4(self, ip: str) -> None:
        """Валидные IPv4-адреса должны проходить валидацию."""
        assert Validator.validate_ip_or_dns(ip) is True

    # === Невалидные IPv4 ===
    # Примечание: "abc.def.ghi.jkl" перенесён в test_valid_dns,
    # так как это валидное DNS-имя (буквы + точки)

    @pytest.mark.parametrize(
        "ip",
        [
            "256.1.1.1",  # Число > 255
            "1.2.3",  # Только 3 октета
            "1.2.3.4.5",  # 5 октетов
            "1.2.3.01",  # Ведущий ноль
            "",  # Пустая строка
            "кириллица.тест",  # Кириллица
        ],
    )
    def test_invalid_ipv4(self, ip: str) -> None:
        """Невалидные IPv4-адреса не должны проходить валидацию."""
        assert Validator.validate_ip_or_dns(ip) is False

    # === Валидные DNS ===
    # "abc.def.ghi.jkl" — валидное DNS-имя (буквы + точки)

    @pytest.mark.parametrize(
        "dns",
        [
            "localhost",
            "a",  # Минимальное DNS-имя (1 символ)
            "oracle-db.company.local",
            "db_server_01",
            "my-host.name",
            "A.B.C",  # Заглавные буквы
            "abc.def.ghi.jkl",  # Валидное DNS-имя (буквы + точки)
        ],
    )
    def test_valid_dns(self, dns: str) -> None:
        """Валидные DNS-имена должны проходить валидацию."""
        assert Validator.validate_ip_or_dns(dns) is True

    # === Невалидные DNS (строгая валидация) ===

    @pytest.mark.parametrize(
        "dns",
        [
            "---",  # Только дефисы (нет буквенно-цифровых)
            "...",  # Только точки
            "-host",  # Начинается с '-'
            "host-",  # Заканчивается на '-'
            ".host",  # Начинается с '.'
            "host.",  # Заканчивается на '.'
            "oracle..db.local",  # Двойная точка
            "a" * 256,  # Превышение максимальной длины (256 символов)
            "",  # Пустая строка
            "кириллица",  # Кириллица
            "host name",  # Пробел
            "host@name",  # Спецсимвол @
        ],
    )
    def test_invalid_dns(self, dns: str) -> None:
        """Невалидные DNS-имена не должны проходить валидацию."""
        assert Validator.validate_ip_or_dns(dns) is False

    # === Граничные случаи DNS ===

    def test_dns_exactly_255_chars(self) -> None:
        """DNS-имя длиной ровно 255 символов должно быть валидным."""
        dns = "a" * 255
        assert Validator.validate_ip_or_dns(dns) is True

    def test_dns_with_leading_trailing_spaces(self) -> None:
        """DNS-имя с пробелами по краям должно валидироваться после strip()."""
        assert Validator.validate_ip_or_dns("  localhost  ") is True


# ============================================================================
# Тесты для Validator.validate_port
# ============================================================================


class TestValidatePort:
    """Тесты валидации номера порта."""

    @pytest.mark.parametrize(
        "port",
        [
            "1",
            "80",
            "1521",
            "65535",
            "01521",  # Ведущий ноль допустим при вводе
        ],
    )
    def test_valid_port(self, port: str) -> None:
        """Валидные номера портов должны проходить валидацию."""
        assert Validator.validate_port(port) is True

    @pytest.mark.parametrize(
        "port",
        [
            "0",  # Ниже минимума
            "65536",  # Выше максимума
            "-1",  # Отрицательное
            "abc",  # Не число
            "1.5",  # Дробное
            "",  # Пустая строка
            " 1521",  # Пробел в начале
        ],
    )
    def test_invalid_port(self, port: str) -> None:
        """Невалидные номера портов не должны проходить валидацию."""
        assert Validator.validate_port(port) is False


# ============================================================================
# Тесты для Validator.validate_username
# ============================================================================


class TestValidateUsername:
    """Тесты валидации имени пользователя."""

    @pytest.mark.parametrize(
        "username",
        [
            "a",  # Минимальная длина (1 символ)
            "admin",
            "user_name",
            "user-name",
            "User123",
            "a" * 30,  # Максимальная длина
        ],
    )
    def test_valid_username(self, username: str) -> None:
        """Валидные имена пользователей должны проходить валидацию."""
        assert Validator.validate_username(username) is True

    @pytest.mark.parametrize(
        "username",
        [
            "",  # Пустая строка
            "a" * 31,  # Превышение максимальной длины
            "user name",  # Пробел
            "user@name",  # Спецсимвол @
            "кириллица",  # Кириллица
            "user.name",  # Точка недопустима
        ],
    )
    def test_invalid_username(self, username: str) -> None:
        """Невалидные имена пользователей не должны проходить валидацию."""
        assert Validator.validate_username(username) is False


# ============================================================================
# Тесты для Validator.validate_password
# ============================================================================


class TestValidatePassword:
    """Тесты валидации пароля."""

    @pytest.mark.parametrize(
        "password",
        [
            "a",  # Минимальная длина (1 символ)
            "password123",
            "p@$$w0rd!",
            " ",  # Пробел допустим
            "a" * 1000,  # Длинный пароль (NF-2b)
        ],
    )
    def test_valid_password(self, password: str) -> None:
        """Валидные пароли должны проходить валидацию."""
        assert Validator.validate_password(password) is True

    def test_empty_password(self) -> None:
        """Пустой пароль не должен проходить валидацию."""
        assert Validator.validate_password("") is False


# ============================================================================
# Тесты для Validator.validate_service_name
# ============================================================================


class TestValidateServiceName:
    """Тесты валидации идентификатора службы."""

    @pytest.mark.parametrize(
        "service_name",
        [
            "",  # Пустая строка допустима (поле опционально)
            "ORCL",
            "service.name",
            "service_name",
            "service-name",
            "a" * 30,  # Максимальная длина
        ],
    )
    def test_valid_service_name(self, service_name: str) -> None:
        """Валидные идентификаторы службы должны проходить валидацию."""
        assert Validator.validate_service_name(service_name) is True

    @pytest.mark.parametrize(
        "service_name",
        [
            "a" * 31,  # Превышение максимальной длины
            "service name",  # Пробел
            "service@name",  # Спецсимвол @
            "кириллица",  # Кириллица
        ],
    )
    def test_invalid_service_name(self, service_name: str) -> None:
        """Невалидные идентификаторы службы не должны проходить валидацию."""
        assert Validator.validate_service_name(service_name) is False


# ============================================================================
# Тесты для Validator.validate_all
# ============================================================================


class TestValidateAll:
    """Тесты комплексной валидации всех полей."""

    def test_all_fields_valid(self) -> None:
        """Все поля валидны — validate_all возвращает True."""
        assert (
            Validator.validate_all(
                ip="192.168.1.1",
                port="1521",
                username="admin",
                password="password",
                service_name="ORCL",
            )
            is True
        )

    def test_all_fields_valid_with_dns(self) -> None:
        """Валидация с DNS-именем вместо IP."""
        assert (
            Validator.validate_all(
                ip="oracle-db.local",
                port="1521",
                username="admin",
                password="password",
                service_name="ORCL",
            )
            is True
        )

    def test_empty_service_name_valid(self) -> None:
        """Пустой идентификатор службы допустим (поле опционально)."""
        assert (
            Validator.validate_all(
                ip="192.168.1.1",
                port="1521",
                username="admin",
                password="password",
                service_name="",
            )
            is True
        )

    @pytest.mark.parametrize(
        "kwargs",
        [
            {
                "ip": "",
                "port": "1521",
                "username": "admin",
                "password": "pass",
                "service_name": "ORCL",
            },
            {
                "ip": "192.168.1.1",
                "port": "",
                "username": "admin",
                "password": "pass",
                "service_name": "ORCL",
            },
            {
                "ip": "192.168.1.1",
                "port": "1521",
                "username": "",
                "password": "pass",
                "service_name": "ORCL",
            },
            {
                "ip": "192.168.1.1",
                "port": "1521",
                "username": "admin",
                "password": "",
                "service_name": "ORCL",
            },
        ],
    )
    def test_one_field_invalid(self, kwargs: dict[str, str]) -> None:
        """Если хотя бы одно обязательное поле невалидно —
        validate_all возвращает False."""
        assert Validator.validate_all(**kwargs) is False


# ============================================================================
# Тесты для ConnectionConfig
# ============================================================================


class TestConnectionConfig:
    """Тесты класса ConnectionConfig."""

    def test_default_values(self) -> None:
        """Значения по умолчанию должны соответствовать F-9, F-13."""
        config = ConnectionConfig()
        assert config.ip == ""
        assert config.port == 1521
        assert config.username == ""
        assert config.service_name == "ORCL"

    def test_to_dict(self) -> None:
        """Сериализация в словарь должна содержать только 4 поля (без пароля)."""
        config = ConnectionConfig(
            ip="192.168.1.1", port=1521, username="admin", service_name="ORCL"
        )
        data = config.to_dict()

        assert data == {
            "ip": "192.168.1.1",
            "port": 1521,
            "username": "admin",
            "service_name": "ORCL",
        }
        assert "password" not in data

    def test_from_dict_valid(self) -> None:
        """Десериализация из валидного словаря."""
        data: dict[str, object] = {
            "ip": "192.168.1.1",
            "port": 1521,
            "username": "admin",
            "service_name": "ORCL",
        }
        config = ConnectionConfig.from_dict(data)

        assert config.ip == "192.168.1.1"
        assert config.port == 1521
        assert config.username == "admin"
        assert config.service_name == "ORCL"

    def test_from_dict_with_string_port(self) -> None:
        """Десериализация должна корректно обрабатывать port как строку (F-13)."""
        data: dict[str, object] = {
            "ip": "192.168.1.1",
            "port": "1521",
            "username": "admin",
            "service_name": "ORCL",
        }
        config = ConnectionConfig.from_dict(data)
        assert config.port == 1521
        assert isinstance(config.port, int)

    def test_from_dict_missing_fields(self) -> None:
        """Отсутствующие поля должны заполняться значениями по умолчанию."""
        data: dict[str, object] = {}
        config = ConnectionConfig.from_dict(data)

        assert config.ip == ""
        assert config.port == 1521
        assert config.username == ""
        assert config.service_name == "ORCL"

    def test_from_dict_invalid_port(self) -> None:
        """Некорректный port должен вызывать ValueError."""
        data: dict[str, object] = {"port": "abc"}
        with pytest.raises(ValueError):
            ConnectionConfig.from_dict(data)

    def test_load_from_nonexistent_file(self) -> None:
        """Загрузка из несуществующего файла — значения по умолчанию (F-9)."""
        config = ConnectionConfig()
        config.load_from_file(Path("/nonexistent/path/connection.json"))

        assert config.port == 1521
        assert config.service_name == "ORCL"

    def test_load_from_corrupted_file(self) -> None:
        """Загрузка из повреждённого файла —
        файл удаляется, значения по умолчанию (F-9)."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("некорректный json {{{")
            temp_path = Path(f.name)

        try:
            config = ConnectionConfig()
            config.load_from_file(temp_path)

            assert not temp_path.exists()
            assert config.port == 1521
            assert config.service_name == "ORCL"
        finally:
            if temp_path.exists():
                temp_path.unlink()

    def test_save_and_load_atomically(self) -> None:
        """Атомарное сохранение и загрузка (F-7, F-13)."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "connection.json"

            config = ConnectionConfig(
                ip="192.168.1.1", port=1521, username="admin", service_name="ORCL"
            )
            assert config.save_atomically(file_path) is True

            assert file_path.exists()

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert data["ip"] == "192.168.1.1"
            assert data["port"] == 1521
            assert isinstance(data["port"], int)
            assert "password" not in data

            loaded_config = ConnectionConfig()
            loaded_config.load_from_file(file_path)

            assert loaded_config.ip == "192.168.1.1"
            assert loaded_config.port == 1521
            assert loaded_config.username == "admin"
            assert loaded_config.service_name == "ORCL"

    def test_save_creates_directory(self) -> None:
        """Сохранение должно создавать директорию, если она не существует."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "subdir" / "connection.json"

            config = ConnectionConfig()
            assert config.save_atomically(file_path) is True
            assert file_path.exists()

    @pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific test")
    def test_get_default_file_path_windows(self) -> None:
        """Путь по умолчанию для Windows."""
        with patch.dict(
            os.environ, {"LOCALAPPDATA": "C:\\Users\\test\\AppData\\Local"}
        ):
            path = ConnectionConfig.get_default_file_path()
            assert "alphameterqc" in str(path)
            assert "connection.json" in str(path)

    @pytest.mark.skipif(sys.platform == "win32", reason="Linux-specific test")
    def test_get_default_file_path_linux(self) -> None:
        """Путь по умолчанию для Linux."""
        with patch.object(Path, "home", return_value=Path("/home/test")):
            path = ConnectionConfig.get_default_file_path()
            assert str(path) == "/home/test/.config/alphameterqc/connection.json"


# ============================================================================
# Дополнительные тесты для покрытия edge-кейсов
# ============================================================================


class TestValidatorEdgeCases:
    """Тесты граничных случаев валидатора."""

    def test_validate_ip_or_dns_with_whitespace(self) -> None:
        """DNS с пробелами по краям должен валидироваться после strip()."""
        assert Validator.validate_ip_or_dns("  localhost  ") is True

    def test_validate_port_with_leading_zeros(self) -> None:
        """Порт с ведущими нулями должен валидироваться."""
        assert Validator.validate_port("01521") is True

    def test_validate_username_exactly_30_chars(self) -> None:
        """Имя пользователя ровно 30 символов должно быть валидным."""
        username = "a" * 30
        assert Validator.validate_username(username) is True

    def test_validate_service_name_exactly_30_chars(self) -> None:
        """Идентификатор службы ровно 30 символов должен быть валидным."""
        service_name = "a" * 30
        assert Validator.validate_service_name(service_name) is True

    def test_validate_password_with_spaces(self) -> None:
        """Пароль с пробелами должен быть валидным."""
        assert Validator.validate_password("  ") is True

    def test_validate_all_with_empty_service_name(self) -> None:
        """validate_all должен принимать пустой service_name."""
        assert (
            Validator.validate_all(
                ip="192.168.1.1",
                port="1521",
                username="admin",
                password="pass",
                service_name="",
            )
            is True
        )


class TestConnectionConfigEdgeCases:
    """Тесты граничных случаев ConnectionConfig."""

    def test_save_atomically_with_nested_directory(self) -> None:
        """save_atomically должен создавать вложенные директории."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "level1" / "level2" / "connection.json"

            config = ConnectionConfig(ip="192.168.1.1", port=1521)
            result = config.save_atomically(config_path)

            assert result is True
            assert config_path.exists()

    def test_save_atomically_returns_false_on_permission_error(self) -> None:
        """save_atomically должен возвращать False при ошибке прав."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"
            config = ConnectionConfig(ip="192.168.1.1", port=1521)

            # Мокаем os.replace — он вызывается в конце атомарной записи
            with patch("os.replace", side_effect=PermissionError("Permission denied")):
                result = config.save_atomically(config_path)

            # Должен вернуть False, но не выбросить исключение
            assert result is False

    def test_load_from_file_with_invalid_port_type(self) -> None:
        """load_from_file должен обрабатывать port как строку."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"

            # Создаём файл с port как строка
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"ip": "192.168.1.1", "port": "1521"}, f)

            config = ConnectionConfig()
            config.load_from_file(config_path)

            assert config.port == 1521
            assert isinstance(config.port, int)

    def test_load_from_file_with_missing_fields(self) -> None:
        """
        load_from_file должен заполнять отсутствующие поля значениями по умолчанию.
        """
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"

            # Создаём файл только с ip
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({"ip": "192.168.1.1"}, f)

            config = ConnectionConfig()
            config.load_from_file(config_path)

            assert config.ip == "192.168.1.1"
            assert config.port == 1521  # Значение по умолчанию
            assert config.username == ""  # Значение по умолчанию
            assert config.service_name == "ORCL"  # Значение по умолчанию
