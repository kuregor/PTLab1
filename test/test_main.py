# -*- coding: utf-8 -*-
import os

import pytest

from src.main import format_result, get_path_from_arguments, main


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string[0])

    assert e.type == SystemExit


def test_format_result_with_student() -> None:
    message = format_result("Морозова Елена Игоревна")
    assert "Морозова Елена Игоревна" in message
    assert "76" in message and "3" in message


def test_format_result_without_student() -> None:
    assert "нет" in format_result(None)


def test_main_on_yaml_datafile(monkeypatch, capsys, data_dir: str) -> None:
    path = os.path.join(data_dir, "data.yaml")
    monkeypatch.setattr("sys.argv", ["main.py", "-p", path])
    main()
    captured = capsys.readouterr().out
    assert "Rating: " in captured
    assert "Морозова Елена Игоревна" in captured


def test_main_on_text_datafile(monkeypatch, capsys, data_dir: str) -> None:
    path = os.path.join(data_dir, "data.txt")
    monkeypatch.setattr("sys.argv", ["main.py", "-p", path])
    main()
    assert "Морозова Елена Игоревна" in capsys.readouterr().out


def test_main_on_unsupported_format(monkeypatch, data_dir: str) -> None:
    path = os.path.join(data_dir, "data.csv")
    monkeypatch.setattr("sys.argv", ["main.py", "-p", path])
    with pytest.raises(ValueError):
        main()
