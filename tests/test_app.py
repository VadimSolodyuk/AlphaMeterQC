"""Проверки запуска AlphaMeterQC без открытия GUI."""

import runpy
from unittest.mock import patch

import pytest

from alphameterqc import app


def test_cancel(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(app, "show_dialog", return_value=None) as dialog:
        assert app.main() == 0
    dialog.assert_called_once_with()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""


def test_confirm(capsys: pytest.CaptureFixture[str]) -> None:
    parameters = {"password": "sentinel-password", "ip": "sentinel-host"}
    with patch.object(app, "show_dialog", return_value=parameters) as dialog:
        assert app.main() == 0
    dialog.assert_called_once_with()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "ещё не реализованы" in captured.err
    assert "sentinel-password" not in captured.err
    assert "sentinel-host" not in captured.err


def test_unhandled_error(capsys: pytest.CaptureFixture[str]) -> None:
    with patch.object(app, "show_dialog", side_effect=RuntimeError("secret")):
        assert app.main() == 1
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "Не удалось запустить" in captured.err
    assert "secret" not in captured.err


@pytest.mark.parametrize("exit_code", [0, 1])
def test_entry_point(exit_code: int) -> None:
    with patch.object(app, "main", return_value=exit_code) as main:
        with pytest.raises(SystemExit) as error:
            runpy.run_module("alphameterqc", run_name="__main__")
    assert error.value.code == exit_code
    main.assert_called_once_with()
