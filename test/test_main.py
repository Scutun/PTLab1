# -*- coding: utf-8 -*-
import json

from src.main import get_path_from_arguments, get_reader, main
import pytest


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
        get_path_from_arguments(noncorrect_arguments_string)
    assert e.type == SystemExit


@pytest.mark.parametrize("path, reader_name", [
    ("data/data.json", "JsonDataReader"),
    ("C:/DATA/STUDENTS.JSON", "JsonDataReader"),
    ("data/data.txt", "TextDataReader"),
])
def test_get_reader(path: str, reader_name: str) -> None:
    # сравниваем имена классов: модули импортируются и как src.X, и как X
    assert type(get_reader(path)).__name__ == reader_name


@pytest.mark.parametrize("path", ["data/data.xml", "data/data"])
def test_get_reader_unsupported_format(path: str) -> None:
    with pytest.raises(ValueError):
        get_reader(path)


def test_main_json(tmpdir, monkeypatch, capsys) -> None:
    data = {
        "A": {"математика": 60}, "B": {"математика": 70},
        "C": {"математика": 80}, "D": {"математика": 90},
        "E": {"математика": 100}
    }
    p = tmpdir.join("data.json")
    p.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(p)])
    main()
    output = capsys.readouterr().out
    assert "Q2 (медиана) = 80.00, Q3 = 90.00" in output
    assert "  D: 90.00" in output
    assert "  C: 80.00" not in output


def test_main_txt_without_result(tmpdir, monkeypatch, capsys) -> None:
    p = tmpdir.join("data.txt")
    p.write_text("A\n    химия:80\nB\n    химия:80\n", encoding='utf-8')
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(p)])
    main()
    assert "таких студентов нет" in capsys.readouterr().out
