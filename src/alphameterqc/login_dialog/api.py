"""
Публичный API модуля login_dialog.

Этот модуль предоставляет единственную точку входа для вызывающей системы:
функцию show_dialog().

Пример использования (режим библиотеки):
    from alphameterqc.login_dialog import show_dialog

    result = show_dialog(
        default_ip="192.168.1.1",
        default_port=1521,
        default_username="admin",
        default_service_name="ORCL",
    )

    if result:
        print(f"Подключение к {result['ip']}:{result['port']}")
    else:
        print("Пользователь отменил ввод")

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7) — контракт взаимодействия
- 08_technical_specification.md (v2.9), п. 4.2
"""

from __future__ import annotations

from typing import Any, Optional

from .controller import LoginDialog


def show_dialog(
    default_ip: str = "",
    default_port: int = 1521,
    default_username: str = "",
    default_service_name: str = "ORCL",
    debug: bool = False,
) -> Optional[dict[str, Any]]:
    """
    Отображает диалог ввода идентификационных данных.

    Это основная точка входа для вызывающей системы в режиме библиотеки.

    Args:
        default_ip: Значение по умолчанию для IP-адреса
        default_port: Значение по умолчанию для порта
        default_username: Значение по умолчанию для имени пользователя
        default_service_name: Значение по умолчанию для идентификатора
        debug: Если True, ошибки логируются в stderr (без пароля)

    Returns:
        Словарь с данными подключения при подтверждении:
        {
            "ip": str,
            "port": int,
            "username": str,
            "password": str,
            "service_name": str
        }
        None при отмене или критической ошибке

    Examples:
        >>> result = show_dialog()
        >>> if result:
        ...     print(f"IP: {result['ip']}")
    """
    return LoginDialog.show_dialog(
        default_ip=default_ip,
        default_port=default_port,
        default_username=default_username,
        default_service_name=default_service_name,
        debug=debug,
    )
