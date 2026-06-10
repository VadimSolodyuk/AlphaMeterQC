"""
Модуль View слоя MVC для login_dialog.

Содержит класс:
- ConnectionDialog: графический интерфейс на базе CustomTkinter

Согласно спецификации:
- 09_ui_design.md (v1.1) — спецификация дизайна UI
- 07_domain_model.md (v2.5), класс En.LOGIN.D1.01 ConnectionDialog
- 08_technical_specification.md (v2.9), п. 4.1
"""

from __future__ import annotations

from typing import Any, Callable, Optional

import customtkinter as ctk

from .model import ConnectionConfig, Validator


class ConnectionDialog(ctk.CTk):  # type: ignore[misc]
    """
    Диалог ввода идентификационных данных для подключения к БД.

    Реализует:
    - Отображение 5 полей ввода и 2 кнопок (F-1)
    - Валидацию в реальном времени (F-2)
    - Подсветку ошибок (F-3)
    - Управление активностью кнопки "Ок" (F-4)
    - Маскировку пароля (F-11)
    - Умный фокус (NF-1)
    - Навигацию Tab

    Размеры окна: 450×420 пикселей
    """

    # === Константы UI ===
    WINDOW_WIDTH: int = 450
    WINDOW_HEIGHT: int = 420
    PADDING_X: int = 35  # Центрирование полей: (450 - 380) / 2
    PADDING_Y: int = 15
    FIELD_WIDTH: int = 380
    FIELD_HEIGHT: int = 32
    BUTTON_WIDTH: int = 140
    BUTTON_HEIGHT: int = 36
    FIELD_SPACING: int = 10

    # === Цвета ===
    COLOR_NORMAL: str = "#CCCCCC"  # Серая рамка
    COLOR_FOCUS: str = "#0078D4"  # Синяя рамка (фокус)
    COLOR_ERROR: str = "#FF4444"  # Красная рамка (ошибка)
    COLOR_OK_ACTIVE: str = "#0078D4"  # Синяя кнопка
    COLOR_OK_DISABLED: str = "#A9A9A9"  # Серая кнопка
    COLOR_CANCEL: str = "#6C757D"  # Тёмно-серая кнопка

    def __init__(
        self,
        default_ip: str = "",
        default_port: int = 1521,
        default_username: str = "",
        default_service_name: str = "ORCL",
        on_confirm: Optional[Callable[[dict[str, Any]], None]] = None,
        on_cancel: Optional[Callable[[], None]] = None,
    ) -> None:
        """
        Инициализация диалога.

        Args:
            default_ip: Значение по умолчанию для IP-адреса
            default_port: Значение по умолчанию для порта
            default_username: Значение по умолчанию для имени пользователя
            default_service_name: Значение по умолчанию для идентификатора службы
            on_confirm: Callback при подтверждении (передаётся dict с данными)
            on_cancel: Callback при отмене
        """
        # === Устанавливаем светлую тему ===
        ctk.set_appearance_mode("light")
        # ctk.set_appearance_mode("dark")
        # ctk.set_appearance_mode("system")

        super().__init__()

        # === Сохраняем параметры ===
        self.default_ip = default_ip
        self.default_port = str(default_port)
        self.default_username = default_username
        self.default_service_name = default_service_name
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        # === Базовые настройки окна ===
        self.title("Подключение к БД")
        self.resizable(False, False)
        # Вычисляем позицию центра ДО первого geometry()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.WINDOW_WIDTH) // 2
        y = (screen_height - self.WINDOW_HEIGHT) // 2

        # Задаём размер и позицию ОДНОВРЕМЕННО
        self.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}+{x}+{y}")

        # === Создаём элементы интерфейса ===
        self._create_widgets()

        # === Загружаем сохранённые параметры (если не переданы дефолты) ===
        if not any([default_ip, default_username]):
            self._load_saved_config()

        # === Устанавливаем умный фокус ===
        self._set_smart_focus()

        # === Привязываем обработчики событий ===
        self._bind_events()

    def _create_widgets(self) -> None:
        """Создание всех элементов интерфейса."""
        # === Поле 1: IP-адрес/хост ===
        self.ip_label = ctk.CTkLabel(
            self,
            text="IP-адрес/хост:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.ip_label.place(x=self.PADDING_X, y=self.PADDING_Y)

        self.ip_entry = ctk.CTkEntry(
            self,
            width=self.FIELD_WIDTH,
            height=self.FIELD_HEIGHT,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите IP-адрес или DNS-имя",
            border_color=self.COLOR_NORMAL,
        )
        self.ip_entry.place(x=self.PADDING_X, y=self.PADDING_Y + 22)

        # === Поле 2: Порт ===
        y_offset_2 = self.PADDING_Y + 55 + self.FIELD_SPACING
        self.port_label = ctk.CTkLabel(
            self,
            text="Порт:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.port_label.place(x=self.PADDING_X, y=y_offset_2)

        self.port_entry = ctk.CTkEntry(
            self,
            width=self.FIELD_WIDTH,
            height=self.FIELD_HEIGHT,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите номер порта (1–65535)",
            border_color=self.COLOR_NORMAL,
        )
        self.port_entry.place(x=self.PADDING_X, y=y_offset_2 + 22)

        # === Поле 3: Имя пользователя ===
        y_offset_3 = y_offset_2 + 55 + self.FIELD_SPACING
        self.username_label = ctk.CTkLabel(
            self,
            text="Имя пользователя:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.username_label.place(x=self.PADDING_X, y=y_offset_3)

        self.username_entry = ctk.CTkEntry(
            self,
            width=self.FIELD_WIDTH,
            height=self.FIELD_HEIGHT,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите имя пользователя",
            border_color=self.COLOR_NORMAL,
        )
        self.username_entry.place(x=self.PADDING_X, y=y_offset_3 + 22)

        # === Поле 4: Пароль (с маскировкой) ===
        y_offset_4 = y_offset_3 + 55 + self.FIELD_SPACING
        self.password_label = ctk.CTkLabel(
            self,
            text="Пароль:",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.password_label.place(x=self.PADDING_X, y=y_offset_4)

        self.password_entry = ctk.CTkEntry(
            self,
            width=self.FIELD_WIDTH,
            height=self.FIELD_HEIGHT,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите пароль",
            show="•",  # Маскировка пароля
            border_color=self.COLOR_NORMAL,
        )
        self.password_entry.place(x=self.PADDING_X, y=y_offset_4 + 22)

        # === Поле 5: Идентификатор службы ===
        y_offset_5 = y_offset_4 + 55 + self.FIELD_SPACING
        self.service_label = ctk.CTkLabel(
            self,
            text="Идентификатор службы (SID/Service Name):",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.service_label.place(x=self.PADDING_X, y=y_offset_5)

        self.service_entry = ctk.CTkEntry(
            self,
            width=self.FIELD_WIDTH,
            height=self.FIELD_HEIGHT,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите идентификатор службы (опционально)",
            border_color=self.COLOR_NORMAL,
        )
        self.service_entry.place(x=self.PADDING_X, y=y_offset_5 + 22)

        # === Кнопки ===
        button_y = 340

        self.cancel_button = ctk.CTkButton(
            self,
            text="Отмена",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            font=ctk.CTkFont(size=14),
            fg_color=self.COLOR_CANCEL,
            hover_color="#5A6268",
            command=self._on_cancel,
        )
        self.cancel_button.place(x=self.PADDING_X, y=button_y)

        self.ok_button = ctk.CTkButton(
            self,
            text="Ок",
            width=self.BUTTON_WIDTH,
            height=self.BUTTON_HEIGHT,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.COLOR_OK_DISABLED,
            hover_color=self.COLOR_OK_ACTIVE,
            state="disabled",  # По умолчанию неактивна
            command=self._on_confirm,
        )
        self.ok_button.place(x=self.PADDING_X + 240, y=button_y)

    def _load_saved_config(self) -> None:
        """Загружает сохранённые параметры из файла."""

        config = ConnectionConfig()
        config.load_from_file(ConnectionConfig.get_default_file_path())

        # Заполняем поля значениями из конфигурации
        if config.ip:
            self.ip_entry.delete(0, "end")
            self.ip_entry.insert(0, config.ip)

        if config.username:
            self.username_entry.delete(0, "end")
            self.username_entry.insert(0, config.username)

        # Порт и service_name всегда заполняем (даже значениями по умолчанию)
        self.port_entry.delete(0, "end")
        self.port_entry.insert(0, str(config.port))

        self.service_entry.delete(0, "end")
        self.service_entry.insert(0, config.service_name)

    def _set_smart_focus(self) -> None:
        """
        Устанавливает умный фокус (NF-1).

        Если поле ip или username не пустое → фокус на "Пароль"
        Иначе → фокус на "IP-адрес/хост"
        """
        ip_value = self.ip_entry.get().strip()
        username_value = self.username_entry.get().strip()

        if ip_value or username_value:
            # Фокус на пароль для ускорения ввода
            self.password_entry.focus_set()
        else:
            # Первый запуск — фокус на IP
            self.ip_entry.focus_set()

    def _bind_events(self) -> None:
        """Привязка обработчиков событий."""
        # Валидация при изменении полей через KeyRelease
        for entry in [
            self.ip_entry,
            self.port_entry,
            self.username_entry,
            self.password_entry,
            self.service_entry,
        ]:
            entry.bind(
                "<KeyRelease>",
                lambda e: self._validate_fields(),
            )

        # Обработка Enter (если форма валидна)
        self.bind(
            "<Return>",
            lambda e: self._on_confirm() if self._is_form_valid() else None,
        )

        # Обработка Esc
        self.bind("<Escape>", lambda e: self._on_cancel())

        # Обработка закрытия окна
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _validate_fields(self) -> None:
        """
        Валидация всех полей в реальном времени (F-2, F-3, F-4).

        - Подсвечивает невалидные поля красной рамкой
        - Активирует/деактивирует кнопку "Ок"
        """
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        service_name = self.service_entry.get()

        # Валидация каждого поля
        ip_valid = Validator.validate_ip_or_dns(ip)
        port_valid = Validator.validate_port(port)
        username_valid = Validator.validate_username(username)
        password_valid = Validator.validate_password(password)
        service_name_valid = Validator.validate_service_name(service_name)

        # Подсветка ошибок
        self._highlight_field(self.ip_entry, ip_valid)
        self._highlight_field(self.port_entry, port_valid)
        self._highlight_field(self.username_entry, username_valid)
        self._highlight_field(self.password_entry, password_valid)
        self._highlight_field(self.service_entry, service_name_valid)

        # Активация кнопки "Ок"
        all_valid = all(
            [
                ip_valid,
                port_valid,
                username_valid,
                password_valid,
                service_name_valid,
            ]
        )

        if all_valid:
            self.ok_button.configure(
                state="normal",
                fg_color=self.COLOR_OK_ACTIVE,
            )
        else:
            self.ok_button.configure(
                state="disabled",
                fg_color=self.COLOR_OK_DISABLED,
            )

    def _highlight_field(self, entry: ctk.CTkEntry, is_valid: bool) -> None:
        """
        Подсвечивает поле (F-3).

        Args:
            entry: Поле для подсветки
            is_valid: True если поле валидно
        """
        if is_valid:
            entry.configure(border_color=self.COLOR_NORMAL)
        else:
            entry.configure(border_color=self.COLOR_ERROR)

    def _is_form_valid(self) -> bool:
        """
        Проверяет валидность всей формы.

        Returns:
            True если все поля валидны
        """
        return Validator.validate_all(
            ip=self.ip_entry.get(),
            port=self.port_entry.get(),
            username=self.username_entry.get(),
            password=self.password_entry.get(),
            service_name=self.service_entry.get(),
        )

    def _on_confirm(self) -> None:
        """Обработчик нажатия кнопки "Ок" (F-5)."""
        if not self._is_form_valid():
            return

        # Собираем данные
        data = {
            "ip": self.ip_entry.get(),
            "port": int(self.port_entry.get()),
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "service_name": self.service_entry.get(),
        }

        # Вызываем callback (если есть)
        if self.on_confirm:
            self.on_confirm(data)

        # Сохраняем конфигурацию (без пароля)
        config = ConnectionConfig(
            ip=data["ip"],
            port=data["port"],
            username=data["username"],
            service_name=data["service_name"],
        )
        config.save_atomically(ConnectionConfig.get_default_file_path())

        self.destroy()

    def _on_cancel(self) -> None:
        """Обработчик нажатия кнопки "Отмена" (F-6)."""
        if self.on_cancel:
            self.on_cancel()

        self.destroy()

    def get_data(self) -> Optional[dict[str, Any]]:
        """
        Возвращает данные формы (для совместимости с прототипом).

        Returns:
            dict с данными формы или None если форма невалидна
        """
        if not self._is_form_valid():
            return None

        return {
            "ip": self.ip_entry.get(),
            "port": int(self.port_entry.get()),
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
            "service_name": self.service_entry.get(),
        }
