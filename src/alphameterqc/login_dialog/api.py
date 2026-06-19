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
    Отображает диалог ввода данных.

    Returns:
        ConnectionData | None: Введенные данные или None, если диалог отменен
    """
    return LoginDialog.show_dialog(
        default_ip=default_ip,
        default_port=default_port,
        default_username=default_username,
        default_service_name=default_service_name,
        debug=debug,
    )
