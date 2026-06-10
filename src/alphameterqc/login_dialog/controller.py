"""
Модуль Controller слоя MVC для login_dialog.

Содержит класс:
- LoginDialog: координация между Model и View,
  поддержка режимов библиотеки и subprocess

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7) — контракт взаимодействия
- 07_domain_model.md (v2.5), класс En.LOGIN.D0.01 LoginDialog
- 08_technical_specification.md (v2.9), п. 4.2
"""

from __future__ import annotations

import json
import logging
import sys
from typing import Any, Optional

from .view import ConnectionDialog

# Настройка логгера (пароль никогда не логируется)
logger = logging.getLogger(__name__)


class LoginDialog:
    """
    Главный класс модуля, предоставляющий API.

    Поддерживает два режима интеграции:
    1. Режим библиотеки (по умолчанию) — вызов show_dialog()
    2. Режим subprocess — запуск через __main__.py

    Реализует интерфейс IConnectionDialog из модели предметной сферы.
    """

    @staticmethod
    def show_dialog(
        default_ip: str = "",
        default_port: int = 1521,
        default_username: str = "",
        default_service_name: str = "ORCL",
        debug: bool = False,
    ) -> Optional[dict[str, Any]]:
        """
        Отображает диалог ввода идентификационных данных.

        Args:
            default_ip: Значение по умолчанию для IP-адреса
            default_port: Значение по умолчанию для порта
            default_username: Значение по умолчанию для имени пользователя
            default_service_name: Значение по умолчанию для идентификатора
            debug: Если True, ошибки логируются в stderr (без пароля)

        Returns:
            Словарь с данными подключения при подтверждении,
            None при отмене или критической ошибке

        Raises:
            Не генерирует исключений наружу (все ошибки обрабатываются)
        """
        if debug:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)

        try:
            # Создаём диалог с callback'ами
            result: Optional[dict[str, Any]] = None

            def on_confirm(data: dict[str, Any]) -> None:
                nonlocal result
                result = data

            def on_cancel() -> None:
                nonlocal result
                result = None

            dialog = ConnectionDialog(
                default_ip=default_ip,
                default_port=default_port,
                default_username=default_username,
                default_service_name=default_service_name,
                on_confirm=on_confirm,
                on_cancel=on_cancel,
            )

            # Запускаем главный цикл GUI
            dialog.mainloop()

            return result

        except Exception as e:
            # Критическая ошибка — логируем (без пароля) и возвращаем None
            if debug:
                logger.exception("Критическая ошибка в LoginDialog")
            else:
                logger.error("Критическая ошибка в LoginDialog: %s", type(e).__name__)
            return None

    @staticmethod
    def run_as_subprocess() -> int:
        """
        Запускает диалог в режиме subprocess.

        Выводит результат в stdout в формате JSON:
        - Успех: {"status": "success", "data": {...}}
        - Отмена: {"status": "cancelled"}
        - Ошибка: {"status": "error", "message": "..."}

        Returns:
            Код возврата процесса: 0 при успехе/отмене, 1 при ошибке
        """
        try:
            result = LoginDialog.show_dialog(debug=False)

            if result is not None:
                # Успех
                output = {
                    "status": "success",
                    "data": result,
                }
                print(json.dumps(output, ensure_ascii=False))
                return 0
            else:
                # Отмена
                output = {"status": "cancelled"}
                print(json.dumps(output, ensure_ascii=False))
                return 0

        except Exception as e:
            # Критическая ошибка
            output = {
                "status": "error",
                "message": f"Критическая ошибка: {type(e).__name__}",
            }
            print(json.dumps(output, ensure_ascii=False), file=sys.stderr)
            return 1
