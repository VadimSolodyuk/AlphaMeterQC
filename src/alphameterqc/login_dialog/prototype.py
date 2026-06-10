"""
Прототип пользовательского интерфейса модуля login_dialog.

Этот файл содержит интерактивный прототип GUI без бизнес-логики.
Цель: проверить визуальное расположение элементов, навигацию Tab,
маскировку пароля и общее поведение интерфейса.

Согласно спецификации: docs/specs/login_dialog/09_ui_design.md
"""

from typing import Any, List

import customtkinter as ctk


class LoginDialogPrototype(ctk.CTk):  # type: ignore[misc]
    """
    Прототип диалога ввода идентификационных данных.

    Размеры окна: 450×420 пикселей (уменьшена высота)
    Тема: Поддерживает Light и Dark
    """

    def __init__(self) -> None:
        super().__init__()

        # === Базовые настройки окна ===
        self.title("Подключение к БД")
        self.geometry("450x420")
        self.resizable(False, False)

        # Отступы от краёв окна
        self.padding_x = (
            35  # Увеличен с 20 до 35 для центрирования полей (450-380)/2 = 35
        )
        self.padding_y = 15  # Уменьшен с 20 до 15
        self.field_spacing = 10  # Уменьшен с 15 до 10

        # === Создание элементов интерфейса ===
        self._create_widgets()

        # === Установка начального фокуса ===
        self.ip_entry.focus_set()

    def _create_widgets(self) -> None:
        """Создание всех элементов интерфейса."""

        # === Поле 1: IP-адрес/хост ===
        self.ip_label = ctk.CTkLabel(
            self, text="IP-адрес/хост:", font=ctk.CTkFont(size=13), anchor="w"
        )
        self.ip_label.place(x=self.padding_x, y=self.padding_y)

        self.ip_entry = ctk.CTkEntry(
            self,
            width=380,
            height=32,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите IP-адрес или DNS-имя",
        )
        self.ip_entry.place(x=self.padding_x, y=self.padding_y + 22)

        # === Поле 2: Порт ===
        y_offset_2 = self.padding_y + 55 + self.field_spacing
        self.port_label = ctk.CTkLabel(
            self, text="Порт:", font=ctk.CTkFont(size=13), anchor="w"
        )
        self.port_label.place(x=self.padding_x, y=y_offset_2)

        self.port_entry = ctk.CTkEntry(
            self,
            width=380,
            height=32,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите номер порта (1–65535)",
        )
        self.port_entry.place(x=self.padding_x, y=y_offset_2 + 22)
        self.port_entry.insert(0, "1521")

        # === Поле 3: Имя пользователя ===
        y_offset_3 = y_offset_2 + 55 + self.field_spacing
        self.username_label = ctk.CTkLabel(
            self, text="Имя пользователя:", font=ctk.CTkFont(size=13), anchor="w"
        )
        self.username_label.place(x=self.padding_x, y=y_offset_3)

        self.username_entry = ctk.CTkEntry(
            self,
            width=380,
            height=32,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите имя пользователя",
        )
        self.username_entry.place(x=self.padding_x, y=y_offset_3 + 22)

        # === Поле 4: Пароль (с маскировкой) ===
        y_offset_4 = y_offset_3 + 55 + self.field_spacing
        self.password_label = ctk.CTkLabel(
            self, text="Пароль:", font=ctk.CTkFont(size=13), anchor="w"
        )
        self.password_label.place(x=self.padding_x, y=y_offset_4)

        self.password_entry = ctk.CTkEntry(
            self,
            width=380,
            height=32,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите пароль",
            show="•",
        )
        self.password_entry.place(x=self.padding_x, y=y_offset_4 + 22)

        # === Поле 5: Идентификатор службы ===
        y_offset_5 = y_offset_4 + 55 + self.field_spacing
        self.service_label = ctk.CTkLabel(
            self,
            text="Идентификатор службы (SID/Service Name):",
            font=ctk.CTkFont(size=13),
            anchor="w",
        )
        self.service_label.place(x=self.padding_x, y=y_offset_5)

        self.service_entry = ctk.CTkEntry(
            self,
            width=380,
            height=32,
            font=ctk.CTkFont(size=13),
            placeholder_text="Введите идентификатор службы (опционально)",
        )
        self.service_entry.place(x=self.padding_x, y=y_offset_5 + 22)
        self.service_entry.insert(0, "ORCL")

        # === Кнопки ===
        button_y = 340

        self.cancel_button = ctk.CTkButton(
            self,
            text="Отмена",
            width=140,
            height=36,
            font=ctk.CTkFont(size=14),
            fg_color="#6C757D",
            hover_color="#5A6268",
            command=self._on_cancel,
        )
        self.cancel_button.place(x=self.padding_x, y=button_y)

        self.ok_button = ctk.CTkButton(
            self,
            text="Ок",
            width=140,
            height=36,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#0078D4",
            hover_color="#006CBE",
            state=ctk.DISABLED,
            command=self._on_ok,
        )
        self.ok_button.place(x=self.padding_x + 240, y=button_y)

        # === Настройка навигации Tab ===
        self.bind_all("<Tab>", self._on_tab_key)
        self.bind_all("<Shift-Tab>", self._on_shift_tab_key)

        self.tab_order: List[ctk.CTkBaseClass] = [
            self.ip_entry,
            self.port_entry,
            self.username_entry,
            self.password_entry,
            self.service_entry,
            self.ok_button,
            self.cancel_button,
        ]
        self.current_tab_index = 0

    def _on_tab_key(self, event: Any) -> str:
        """Обработчик клавиши Tab для навигации между элементами."""
        self.current_tab_index = (self.current_tab_index + 1) % len(self.tab_order)
        self.tab_order[self.current_tab_index].focus_set()
        return "break"

    def _on_shift_tab_key(self, event: Any) -> str:
        """Обработчик клавиши Shift+Tab для навигации назад."""
        self.current_tab_index = (self.current_tab_index - 1) % len(self.tab_order)
        self.tab_order[self.current_tab_index].focus_set()
        return "break"

    def _on_ok(self) -> None:
        """Обработчик нажатия кнопки 'Ок' (заглушка)."""
        print("Нажата кнопка 'Ок'")
        print(f"IP: {self.ip_entry.get()}")
        print(f"Порт: {self.port_entry.get()}")
        print(f"Имя: {self.username_entry.get()}")
        print(f"Пароль: {self.password_entry.get()}")
        print(f"Сервис: {self.service_entry.get()}")
        self.destroy()

    def _on_cancel(self) -> None:
        """Обработчик нажатия кнопки 'Отмена' (заглушка)."""
        print("Нажата кнопка 'Отмена'")
        self.destroy()


def main() -> None:
    """Точка входа для запуска прототипа."""
    ctk.set_appearance_mode("light")
    app = LoginDialogPrototype()
    app.mainloop()


if __name__ == "__main__":
    main()
