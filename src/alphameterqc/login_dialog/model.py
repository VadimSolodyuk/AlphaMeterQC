"""
Модуль Model слоя MVC для login_dialog.

Содержит классы:
- Validator: проверка корректности вводимых данных (F-2)
- ConnectionConfig: работа с файлом сохранённых параметров (F-7, F-8, F-9, F-13)

Согласно спецификации:
- 04_srs.md (v2.9), раздел 1.6 «Правила проверки корректности полей»
- 07_domain_model.md (v2.5), класс En.LOGIN.D1.02 Validator
- 08_technical_specification.md (v2.9), п. 4.1.2
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ============================================================================
# Класс Validator
# ============================================================================


class Validator:
    """Валидатор полей формы ввода данных."""

    """
    Валидатор полей формы ввода данных.

    Реализует правила проверки из SRS (раздел 1.6):
    - IP-адрес (IPv4) или строгое DNS-имя
    - Порт (1-65535)
    - Имя пользователя (1-30 символов)
    - Пароль (не пустой)
    - Идентификатор службы (0-30 символов, опционально)
    """

    # === Константы валидации ===

    MAX_DNS_LENGTH: int = 255

    DNS_PATTERN: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9_\-\.]+$")

    MAX_USERNAME_LENGTH: int = 30
    MAX_SERVICE_NAME_LENGTH: int = 30

    USERNAME_PATTERN: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9_\-]+$")

    SERVICE_NAME_PATTERN: re.Pattern[str] = re.compile(r"^[a-zA-Z0-9_.\-]+$")

    IP_LIKE_PATTERN: re.Pattern[str] = re.compile(r"^[\d\.\-]+$")

    MIN_PORT: int = 1
    MAX_PORT: int = 65535

    # === Методы валидации ===

    @staticmethod
    def validate_ip_or_dns(value: str) -> bool:
        """
        Проверяет, является ли значение валидным IPv4-адресом или DNS-именем.

        Если строка выглядит как IP (только цифры, точки, дефисы),
        но не является валидным IPv4, она отклоняется.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение валидно
        """
        if not value:
            return False

        # Сначала пробуем валидировать как IPv4
        if Validator._validate_ipv4(value):
            return True

        # Если строка выглядит как IP (только цифры, точки, дефисы),
        # но не валидный IPv4 — отклоняем
        if Validator.IP_LIKE_PATTERN.match(value):
            return False

        # Иначе валидируем как DNS
        return Validator._validate_dns(value)

    @staticmethod
    def _validate_ipv4(value: str) -> bool:
        """
        Проверяет, является ли значение валидным IPv4-адресом.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным IPv4
        """
        parts = value.split(".")
        if len(parts) != 4:
            return False

        for part in parts:
            if not part.isdigit():
                return False
            num = int(part)
            if num < 0 or num > 255:
                return False
            if len(part) > 1 and part[0] == "0":
                return False

        return True

    @staticmethod
    def _validate_dns(value: str) -> bool:
        """
        Проверяет, является ли значение валидным DNS-именем (строгая валидация).

        Правила (SRS v2.9, раздел 1.6):
        1. Применяется strip() к входной строке
        2. После strip() должна содержать хотя бы один буквенно-цифровой символ
        3. Не должна начинаться или заканчиваться на '-' или '.'
        4. Допустимые символы: латиница, цифры, '_', '-', '.'
        5. Длина не более 255 символов
        6. Не должна содержать двойные точки '..'

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным DNS-именем
        """
        stripped = value.strip()

        if not stripped or len(stripped) > Validator.MAX_DNS_LENGTH:
            return False

        if not Validator.DNS_PATTERN.match(stripped):
            return False

        if stripped[0] in ("-", ".") or stripped[-1] in ("-", "."):
            return False

        # Проверка на двойные точки
        if ".." in stripped:
            return False

        if not any(c.isalnum() for c in stripped):
            return False

        return True

    @staticmethod
    def validate_port(value: str) -> bool:
        """
        Проверяет, является ли значение валидным номером порта.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным номером порта
        """
        if not value:
            return False

        if not value.isdigit():
            return False

        port = int(value)
        return Validator.MIN_PORT <= port <= Validator.MAX_PORT

    @staticmethod
    def validate_username(value: str) -> bool:
        """
        Проверяет, является ли значение валидным именем пользователя.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным именем пользователя
        """
        if not value or len(value) > Validator.MAX_USERNAME_LENGTH:
            return False

        return bool(Validator.USERNAME_PATTERN.match(value))

    @staticmethod
    def validate_password(value: str) -> bool:
        """
        Проверяет, является ли значение валидным паролем.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным паролем
        """
        return len(value) >= 1

    @staticmethod
    def validate_service_name(value: str) -> bool:
        """
        Проверяет, является ли значение валидным идентификатором службы.

        Args:
            value: Проверяемая строка

        Returns:
            True, если значение является валидным идентификатором службы
        """
        if not value:
            return True

        if len(value) > Validator.MAX_SERVICE_NAME_LENGTH:
            return False

        return bool(Validator.SERVICE_NAME_PATTERN.match(value))

    @staticmethod
    def validate_all(
        ip: str,
        port: str,
        username: str,
        password: str,
        service_name: str,
    ) -> bool:
        """
        Проверяет валидность всех полей формы.

        Args:
            ip: IP-адрес или DNS-имя
            port: Номер порта
            username: Имя пользователя
            password: Пароль
            service_name: Идентификатор службы

        Returns:
            True, если все поля валидны
        """
        return (
            Validator.validate_ip_or_dns(ip)
            and Validator.validate_port(port)
            and Validator.validate_username(username)
            and Validator.validate_password(password)
            and Validator.validate_service_name(service_name)
        )


# ============================================================================
# Класс ConnectionConfig
# ============================================================================


@dataclass
class ConnectionConfig:
    """
    Конфигурация подключения (подмножество ConnectionData без пароля).

    Используется для хранения настроек между сессиями в JSON-файле.
    Никогда не содержит пароль (требование NF-3a).
    """

    ip: str = ""
    port: int = 1521
    username: str = ""
    service_name: str = "ORCL"

    DEFAULT_PORT: int = 1521
    DEFAULT_SERVICE_NAME: str = "ORCL"

    def to_dict(self) -> dict[str, Any]:
        """
        Сериализует конфигурацию в словарь для JSON.

        Returns:
            Словарь с параметрами подключения (без пароля)
        """
        return {
            "ip": self.ip,
            "port": self.port,
            "username": self.username,
            "service_name": self.service_name,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ConnectionConfig":
        """
        Десериализует конфигурацию из словаря.

        Args:
            data: Словарь с параметрами подключения

        Returns:
            Экземпляр ConnectionConfig

        Raises:
            ValueError: Если данные некорректны
        """
        ip = data.get("ip", "")
        username = data.get("username", "")
        service_name = data.get("service_name", cls.DEFAULT_SERVICE_NAME)

        port_raw = data.get("port", cls.DEFAULT_PORT)
        try:
            port = int(port_raw)
        except (ValueError, TypeError):
            raise ValueError(f"Некорректное значение port: {port_raw}")

        return cls(
            ip=ip,
            port=port,
            username=username,
            service_name=service_name,
        )

    def load_from_file(self, file_path: Path) -> None:
        """
        Загружает конфигурацию из JSON-файла.

        Args:
            file_path: Путь к JSON-файлу
        """
        try:
            if not file_path.exists():
                return

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            config = ConnectionConfig.from_dict(data)
            self.ip = config.ip
            self.port = config.port
            self.username = config.username
            self.service_name = config.service_name

        except (json.JSONDecodeError, ValueError):
            try:
                file_path.unlink()
            except OSError:
                pass

            self.ip = ""
            self.port = self.DEFAULT_PORT
            self.username = ""
            self.service_name = self.DEFAULT_SERVICE_NAME

        except OSError:
            self.ip = ""
            self.port = self.DEFAULT_PORT
            self.username = ""
            self.service_name = self.DEFAULT_SERVICE_NAME

    def save_atomically(self, file_path: Path) -> bool:
        """
        Атомарно сохраняет конфигурацию в JSON-файл.

        Args:
            file_path: Путь к целевому JSON-файлу

        Returns:
            True, если сохранение успешно, False при ошибке
        """
        tmp_path: Path | None = None
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)

            tmp_path = file_path.with_suffix(".tmp")

            data = self.to_dict()
            json_content = json.dumps(data, indent=2, ensure_ascii=False)

            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(json_content)

            os.replace(tmp_path, file_path)

            return True

        except OSError:
            if tmp_path and tmp_path.exists():
                try:
                    tmp_path.unlink()
                except OSError:
                    pass
            return False

    @staticmethod
    def get_default_file_path() -> Path:
        """
        Возвращает путь к файлу конфигурации для текущей ОС.

        Windows: %LOCALAPPDATA%\\alphameterqc\\connection.json
        Linux: ~/.config/alphameterqc/connection.json

        Returns:
            Path к файлу конфигурации
        """
        if os.name == "nt":
            # Windows — сначала проверяем LOCALAPPDATA, потом fallback
            local_app_data = os.environ.get("LOCALAPPDATA")
            if local_app_data is None:
                local_app_data = os.path.expanduser("~\\AppData\\Local")
            return Path(local_app_data, "alphameterqc", "connection.json")
        else:
            # Linux (и другие POSIX)
            return Path.home() / ".config" / "alphameterqc" / "connection.json"
