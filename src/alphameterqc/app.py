"""Стартовый сценарий AlphaMeterQC без подключения к БД."""

import sys

from alphameterqc.login_dialog import show_dialog


def main() -> int:
    """Показать диалог; рабочий сценарий пока не реализован.

    Текущий API возвращает None как при отмене, так и при
    обработанной внутри диалога ошибке. Здесь они не различаются.
    """
    try:
        parameters = show_dialog()
    except Exception:
        print("Не удалось запустить AlphaMeterQC.", file=sys.stderr)
        return 1

    if parameters is None:
        return 0

    print(
        "AlphaMeterQC: ввод завершён. Подключение к БД и основной "
        "интерфейс ещё не реализованы.",
        file=sys.stderr,
    )
    return 0
