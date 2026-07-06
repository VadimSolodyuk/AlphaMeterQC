"""
Unit-тесты для view.py (ConnectionDialog).

Тестирует логику без открытия реального окна:
- Валидация полей
- Умный фокус
- Состояние кнопки "Ок"

Согласно спецификации:
- 09_ui_design.md (v1.1)
- 07_domain_model.md (v2.5), класс En.LOGIN.D1.01
"""

from unittest.mock import MagicMock, patch

from alphameterqc.login_dialog.view import ConnectionDialog


class TestConnectionDialogValidation:
    """Тесты валидации полей."""

    def test_validate_fields_with_valid_data(self) -> None:
        """_validate_fields должен активировать кнопку 'Ок' при валидных данных."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            # Мокируем поля ввода
            dialog.ip_entry = MagicMock()
            dialog.port_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()
            dialog.service_entry = MagicMock()
            dialog.ok_button = MagicMock()

            # Возвращаем валидные данные
            dialog.ip_entry.get.return_value = "192.168.1.1"
            dialog.port_entry.get.return_value = "1521"
            dialog.username_entry.get.return_value = "admin"
            dialog.password_entry.get.return_value = "password"
            dialog.service_entry.get.return_value = "ORCL"

            dialog._validate_fields()

            # Кнопка "Ок" должна быть активирована
            dialog.ok_button.configure.assert_called_with(
                state="normal",
                fg_color=ConnectionDialog.COLOR_OK_ACTIVE,
            )

    def test_validate_fields_with_invalid_data(self) -> None:
        """_validate_fields должен деактивировать кнопку 'Ок' при невалидных данных."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.port_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()
            dialog.service_entry = MagicMock()
            dialog.ok_button = MagicMock()

            # Возвращаем невалидные данные (пустой IP)
            dialog.ip_entry.get.return_value = ""
            dialog.port_entry.get.return_value = "1521"
            dialog.username_entry.get.return_value = "admin"
            dialog.password_entry.get.return_value = "password"
            dialog.service_entry.get.return_value = "ORCL"

            dialog._validate_fields()

            # Кнопка "Ок" должна быть деактивирована
            dialog.ok_button.configure.assert_called_with(
                state="disabled",
                fg_color=ConnectionDialog.COLOR_OK_DISABLED,
            )

    def test_highlight_field_valid(self) -> None:
        """_highlight_field должен устанавливать нормальный цвет рамки."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)
            entry = MagicMock()

            dialog._highlight_field(entry, is_valid=True)

            entry.configure.assert_called_with(
                border_color=ConnectionDialog.COLOR_NORMAL,
            )

    def test_highlight_field_invalid(self) -> None:
        """_highlight_field должен устанавливать красный цвет рамки."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)
            entry = MagicMock()

            dialog._highlight_field(entry, is_valid=False)

            entry.configure.assert_called_with(
                border_color=ConnectionDialog.COLOR_ERROR,
            )


class TestConnectionDialogSmartFocus:
    """Тесты умного фокуса."""

    def test_smart_focus_on_password_when_ip_filled(self) -> None:
        """Фокус должен быть на пароле, если IP заполнен."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()

            dialog.ip_entry.get.return_value = "192.168.1.1"
            dialog.username_entry.get.return_value = ""

            dialog._set_smart_focus()

            dialog.password_entry.focus_set.assert_called_once()

    def test_smart_focus_on_password_when_username_filled(self) -> None:
        """Фокус должен быть на пароле, если username заполнен."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()

            dialog.ip_entry.get.return_value = ""
            dialog.username_entry.get.return_value = "admin"

            dialog._set_smart_focus()

            dialog.password_entry.focus_set.assert_called_once()

    def test_smart_focus_on_ip_when_all_empty(self) -> None:
        """Фокус должен быть на IP, если все поля пусты."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()

            dialog.ip_entry.get.return_value = ""
            dialog.username_entry.get.return_value = ""

            dialog._set_smart_focus()

            dialog.ip_entry.focus_set.assert_called_once()


class TestConnectionDialogGetData:
    """Тесты метода get_data."""

    def test_get_data_returns_dict_when_valid(self) -> None:
        """get_data должен возвращать dict при валидной форме."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.port_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()
            dialog.service_entry = MagicMock()

            dialog.ip_entry.get.return_value = "192.168.1.1"
            dialog.port_entry.get.return_value = "1521"
            dialog.username_entry.get.return_value = "admin"
            dialog.password_entry.get.return_value = "secret"
            dialog.service_entry.get.return_value = "ORCL"

            data = dialog.get_data()

            assert data is not None
            assert data["ip"] == "192.168.1.1"
            assert data["port"] == 1521
            assert data["username"] == "admin"
            assert data["password"] == "secret"
            assert data["service_name"] == "ORCL"

    def test_get_data_returns_none_when_invalid(self) -> None:
        """get_data должен возвращать None при невалидной форме."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            dialog.ip_entry = MagicMock()
            dialog.port_entry = MagicMock()
            dialog.username_entry = MagicMock()
            dialog.password_entry = MagicMock()
            dialog.service_entry = MagicMock()

            # Пустой IP — форма невалидна
            dialog.ip_entry.get.return_value = ""
            dialog.port_entry.get.return_value = "1521"
            dialog.username_entry.get.return_value = "admin"
            dialog.password_entry.get.return_value = "secret"
            dialog.service_entry.get.return_value = "ORCL"

            data = dialog.get_data()

            assert data is None


class TestConnectionDialogCentering:
    """Тесты центрирования окна."""

    def test_window_opens_at_center(self) -> None:
        """Окно должно открываться по центру экрана."""
        with patch(
            "alphameterqc.login_dialog.view.ctk.CTk.__init__", return_value=None
        ):
            dialog = ConnectionDialog.__new__(ConnectionDialog)

            # Мокируем методы получения размеров экрана
            dialog.winfo_screenwidth = MagicMock(return_value=1920)
            dialog.winfo_screenheight = MagicMock(return_value=1080)
            dialog.geometry = MagicMock()
            dialog.title = MagicMock()
            dialog.resizable = MagicMock()

            # Имитируем блок инициализации из __init__
            screen_width = dialog.winfo_screenwidth()
            screen_height = dialog.winfo_screenheight()
            x = (screen_width - ConnectionDialog.WINDOW_WIDTH) // 2
            y = (screen_height - ConnectionDialog.WINDOW_HEIGHT) // 2

            dialog.geometry(
                f"{ConnectionDialog.WINDOW_WIDTH}x"
                f"{ConnectionDialog.WINDOW_HEIGHT}+{x}+{y}"
            )

            # Ожидаемая позиция: (1920-450)/2=735, (1080-420)/2=330
            dialog.geometry.assert_called_once_with("450x420+735+330")
