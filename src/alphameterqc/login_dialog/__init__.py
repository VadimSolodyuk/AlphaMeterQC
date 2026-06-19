"""
Модуль login_dialog — ввод данных для подключения к БД.

Публичный API:
    from alphameterqc.login_dialog import show_dialog

    result = show_dialog()

Режимы интеграции:
1. Библиотека: импорт и вызов show_dialog()
2. Subprocess: python -m alphameterqc.login_dialog

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7)
- 08_technical_specification.md (v2.9), п. 4.2
"""

from .api import show_dialog

__all__ = ["show_dialog"]
