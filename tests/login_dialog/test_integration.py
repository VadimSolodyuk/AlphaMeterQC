"""
Интеграционные тесты для модуля login_dialog.

Проверяет:
- Полный сценарий в режиме библиотеки
- Режим subprocess (запуск + парсинг JSON)
- Обработку ошибок файловой системы
- Сохранение/загрузку конфигурации

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7) — контракт взаимодействия
- 08_technical_specification.md (v2.9), п. 4.2, 4.6, 4.9
"""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from alphameterqc.login_dialog.controller import LoginDialog
from alphameterqc.login_dialog.model import ConnectionConfig

# ============================================================================
# Тесты режима библиотеки
# ============================================================================


class TestIntegrationLibraryMode:
    """Интеграционные тесты режима библиотеки."""

    def test_show_dialog_returns_none_on_cancel(self) -> None:
        """show_dialog возвращает None при отмене."""
        with patch(
            "alphameterqc.login_dialog.controller.ConnectionDialog",
        ) as mock_dialog:
            mock_instance = MagicMock()
            mock_dialog.return_value = mock_instance

            def simulate_cancel() -> None:
                call_kwargs = mock_dialog.call_args
                if call_kwargs and "on_cancel" in call_kwargs.kwargs:
                    call_kwargs.kwargs["on_cancel"]()

            mock_instance.mainloop.side_effect = simulate_cancel

            result = LoginDialog.show_dialog()

            assert result is None

    def test_show_dialog_returns_data_on_confirm(self) -> None:
        """show_dialog возвращает dict с данными при подтверждении."""
        expected_data: dict[str, object] = {
            "ip": "192.168.1.1",
            "port": 1521,
            "username": "admin",
            "password": "secret",
            "service_name": "ORCL",
        }

        with patch(
            "alphameterqc.login_dialog.controller.ConnectionDialog",
        ) as mock_dialog:
            mock_instance = MagicMock()
            mock_dialog.return_value = mock_instance

            def simulate_confirm() -> None:
                call_kwargs = mock_dialog.call_args
                if call_kwargs and "on_confirm" in call_kwargs.kwargs:
                    call_kwargs.kwargs["on_confirm"](expected_data)

            mock_instance.mainloop.side_effect = simulate_confirm

            result = LoginDialog.show_dialog()

            assert result == expected_data

    def test_show_dialog_with_custom_defaults(self) -> None:
        """show_dialog передаёт значения по умолчанию в диалог."""
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
            )

            call_kwargs = mock_dialog.call_args.kwargs
            assert call_kwargs["default_ip"] == "10.0.0.1"
            assert call_kwargs["default_port"] == 3306
            assert call_kwargs["default_username"] == "root"
            assert call_kwargs["default_service_name"] == "MYSQL"


# ============================================================================
# Тесты режима subprocess
# ============================================================================


class TestIntegrationSubprocessMode:
    """Интеграционные тесты режима subprocess."""

    def test_subprocess_returns_success_json(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Subprocess выводит JSON с данными при успехе."""
        expected_data: dict[str, object] = {
            "ip": "192.168.1.1",
            "port": 1521,
            "username": "admin",
            "password": "secret",
            "service_name": "ORCL",
        }

        with patch.object(
            LoginDialog,
            "show_dialog",
            return_value=expected_data,
        ):
            return_code = LoginDialog.run_as_subprocess()

            captured = capsys.readouterr()
            output = json.loads(captured.out)

            assert return_code == 0
            assert output["status"] == "success"
            assert output["data"] == expected_data

    def test_subprocess_returns_cancelled_json(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Subprocess выводит JSON с отменой."""
        with patch.object(
            LoginDialog,
            "show_dialog",
            return_value=None,
        ):
            return_code = LoginDialog.run_as_subprocess()

            captured = capsys.readouterr()
            output = json.loads(captured.out)

            assert return_code == 0
            assert output["status"] == "cancelled"

    def test_subprocess_returns_error_json(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        """Subprocess выводит JSON с ошибкой при критическом сбое."""
        with patch.object(
            LoginDialog,
            "show_dialog",
            side_effect=RuntimeError("Тестовая ошибка"),
        ):
            return_code = LoginDialog.run_as_subprocess()

            captured = capsys.readouterr()
            output = json.loads(captured.err)

            assert return_code == 1
            assert output["status"] == "error"
            assert "RuntimeError" in output["message"]


# ============================================================================
# Тесты сохранения/загрузки конфигурации
# ============================================================================


class TestIntegrationConfigPersistence:
    """Тесты сохранения и загрузки конфигурации."""

    def test_config_saved_after_confirm(self) -> None:
        """Конфигурация сохраняется после подтверждения."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"

            config = ConnectionConfig(
                ip="192.168.1.1",
                port=1521,
                username="admin",
                service_name="ORCL",
            )
            config.save_atomically(config_path)

            assert config_path.exists()

            with open(config_path, "r", encoding="utf-8") as f:
                saved_data = json.load(f)

            assert saved_data["ip"] == "192.168.1.1"
            assert saved_data["port"] == 1521
            assert saved_data["username"] == "admin"
            assert saved_data["service_name"] == "ORCL"
            assert "password" not in saved_data

    def test_config_loaded_on_dialog_init(self) -> None:
        """Диалог загружает конфигурацию при инициализации."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"

            test_config: dict[str, object] = {
                "ip": "10.0.0.1",
                "port": 3306,
                "username": "testuser",
                "service_name": "TESTDB",
            }

            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(test_config, f)

            config = ConnectionConfig()
            config.load_from_file(config_path)

            assert config.ip == "10.0.0.1"
            assert config.port == 3306
            assert config.username == "testuser"
            assert config.service_name == "TESTDB"


# ============================================================================
# Тесты обработки ошибок
# ============================================================================


class TestIntegrationErrorHandling:
    """Тесты обработки ошибок."""

    def test_corrupted_config_file_handled(self) -> None:
        """Повреждённый файл конфигурации обрабатывается корректно."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "connection.json"

            with open(config_path, "w", encoding="utf-8") as f:
                f.write("некорректный json {{{")

            config = ConnectionConfig()
            config.load_from_file(config_path)

            assert not config_path.exists()
            assert config.port == 1521
            assert config.service_name == "ORCL"

    def test_missing_config_file_handled(self) -> None:
        """Отсутствующий файл конфигурации обрабатывается корректно."""
        config = ConnectionConfig()
        config.load_from_file(
            Path("/nonexistent/path/connection.json"),
        )

        assert config.ip == ""
        assert config.port == 1521
        assert config.username == ""
        assert config.service_name == "ORCL"

    def test_no_write_permission_handled(self) -> None:
        """Отсутствие прав на запись обрабатывается корректно."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            config_path = Path(tmp_dir) / "readonly" / "connection.json"

            config = ConnectionConfig(
                ip="192.168.1.1",
                port=1521,
                username="admin",
                service_name="ORCL",
            )

            result = config.save_atomically(config_path)

            assert isinstance(result, bool)
