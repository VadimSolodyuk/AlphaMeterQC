"""Ручная интерактивная проверка login_dialog с debug=True.

Запуск из корня проекта:
    python tests/login_dialog/manual_test_integration.py

Используйте только тестовые параметры подключения.
Подтверждение ввода может заменить сохранённые настройки.
Пароль и параметры подключения в терминал не выводятся.
"""

from alphameterqc.login_dialog import show_dialog


def main() -> None:
    """Открыть рабочий диалог и вывести результат без данных подключения."""
    print("Запуск диалога...")
    result = show_dialog(debug=True)

    if result:
        print("Успех: данные получены (без вывода параметров подключения)")
    else:
        print("Отмена или ошибка")


if __name__ == "__main__":
    main()
