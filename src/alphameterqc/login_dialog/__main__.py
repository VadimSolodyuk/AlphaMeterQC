"""
Точка входа для режима subprocess.

Запуск:
    python -m alphameterqc.login_dialog

Или после упаковки через PyInstaller:
    ./login_dialog.exe

Выводит результат в stdout в формате JSON:
- Успех: {"status": "success", "data": {...}}
- Отмена: {"status": "cancelled"}
- Ошибка: {"status": "error", "message": "..."}

Код возврата:
- 0 при успехе или отмене
- 1 при критической ошибке

Согласно спецификации:
- 05-5_UC.LOGIN.D3.01.md (v1.7) — контракт взаимодействия
- 08_technical_specification.md (v2.9), п. 4.2
"""

import sys

from .controller import LoginDialog


def main() -> int:
    """Точка входа для режима subprocess."""
    return LoginDialog.run_as_subprocess()


if __name__ == "__main__":
    sys.exit(main())
