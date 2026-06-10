"""
Unit-тесты для controller.py.

Проверяет:
- Обработку исключений в show_dialog()
- Логирование ошибок
- Корректность вызова ConnectionDialog

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7)
- 08_technical_specification.md (v2.9), п. 4.2
"""

import logging
from unittest.mock import MagicMock, patch

import pytest

from alphameterqc.login_dialog.controller import LoginDialog


class TestLoginDialogShowDialog:
    """Тесты метода show_dialog."""

    def test_show_dialog_handles_exception(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """show_dialog должен обрабатывать исключения и возвращать None."""
        with patch(
            "alphameterqc.login_dialog.controller.ConnectionDialog",
            side_effect=RuntimeError("Тестовая ошибка"),
        ):
            with caplog.at_level(logging.ERROR):
                result = LoginDialog.show_dialog()

            assert result is None
            assert "Критическая ошибка" in caplog.text

    def test_show_dialog_with_debug_mode(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        """show_dialog в режиме debug должен логировать исключения."""
        with patch(
            "alphameterqc.login_dialog.controller.ConnectionDialog",
            side_effect=RuntimeError("Тестовая ошибка"),
        ):
            with caplog.at_level(logging.DEBUG):
                result = LoginDialog.show_dialog(debug=True)

            assert result is None
            # В debug mode должно быть больше логов
            assert len(caplog.records) > 0

    def test_show_dialog_passes_parameters(self) -> None:
        """show_dialog должен передавать параметры в ConnectionDialog."""
        with patch(
            "alphameterqc.login_dialog.controller.ConnectionDialog",
        ) as mock_dialog:
            mock_instance = MagicMock()
            mock_dialog.return_value = mock_instance
            mock_instance.mainloop = lambda: None

            LoginDialog.show_dialog(
                default_ip="10.0.0.1",
                default_port=3306,
                default_username="root",
                default_service_name="MYSQL",
                debug=True,
            )

            call_kwargs = mock_dialog.call_args.kwargs
            assert call_kwargs["default_ip"] == "10.0.0.1"
            assert call_kwargs["default_port"] == 3306
            assert call_kwargs["default_username"] == "root"
            assert call_kwargs["default_service_name"] == "MYSQL"


class TestLoginDialogRunAsSubprocess:
    """Тесты метода run_as_subprocess."""

    def test_run_as_subprocess_handles_exception(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """run_as_subprocess должен обрабатывать исключения и возвращать код 1."""
        with patch.object(
            LoginDialog,
            "show_dialog",
            side_effect=RuntimeError("Критическая ошибка"),
        ):
            return_code = LoginDialog.run_as_subprocess()

            captured = capsys.readouterr()
            assert return_code == 1
            assert "error" in captured.err
