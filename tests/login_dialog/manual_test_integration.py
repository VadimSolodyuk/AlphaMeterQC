"""Быстрая проверка работы модуля."""

from alphameterqc.login_dialog import show_dialog

print("Запуск диалога...")
result = show_dialog(debug=True)

if result:
    print(f"✅ Успех: {result}")
else:
    print("❌ Отмена или ошибка")
