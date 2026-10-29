# -*- coding: utf-8 -*-
import json

import pytest
from src.Types import DataType
from src.JsonDataReader import JsonDataReader


class TestJsonDataReader:
    @pytest.fixture()
    def file_and_data_content(self) -> tuple[str, DataType]:
        text = json.dumps({
            "Иванов Константин Дмитриевич": {
                "математика": 91, "химия": 100
            },
            "Петров Петр Семенович": {
                "русский язык": 87, "литература": 78
            }
        }, ensure_ascii=False)
        data = {
            "Иванов Константин Дмитриевич": [
                ("математика", 91), ("химия", 100)
            ],
            "Петров Петр Семенович": [
                ("русский язык", 87), ("литература", 78)
            ]
        }
        return text, data

    @pytest.fixture()
    def write_file(self, tmpdir):
        def _write(content: str) -> str:
            p = tmpdir.join("my_data.json")
            p.write_text(content, encoding='utf-8')
            return str(p)
        return _write

    def test_init(self) -> None:
        assert JsonDataReader().students == {}

    def test_read(self, file_and_data_content: tuple[str, DataType],
                  write_file) -> None:
        path = write_file(file_and_data_content[0])
        reader = JsonDataReader()
        assert reader.read(path) == file_and_data_content[1]
        assert reader.students == file_and_data_content[1]

    def test_read_twice_does_not_accumulate(
            self, file_and_data_content: tuple[str, DataType],
            write_file) -> None:
        path = write_file(file_and_data_content[0])
        reader = JsonDataReader()
        reader.read(path)
        assert reader.read(path) == file_and_data_content[1]

    def test_read_empty_object(self, write_file) -> None:
        assert JsonDataReader().read(write_file("{}")) == {}

    def test_read_student_without_subjects(self, write_file) -> None:
        path = write_file('{"Сидоров Иван": {}}')
        assert JsonDataReader().read(path) == {"Сидоров Иван": []}

    @pytest.mark.parametrize("content", [
        '[1, 2, 3]',
        '"строка"',
        '{"Сидоров Иван": [90, 80]}',
        '{"Сидоров Иван": {"химия": "90"}}',
        '{"Сидоров Иван": {"химия": 90.5}}',
        '{"Сидоров Иван": {"химия": true}}',
        '{"Сидоров Иван": {"химия": null}}',
        '{"Сидоров Иван": {"химия": -1}}',
        '{"Сидоров Иван": {"химия": 101}}',
    ])
    def test_read_wrong_structure(self, write_file, content: str) -> None:
        with pytest.raises(ValueError):
            JsonDataReader().read(write_file(content))

    def test_read_broken_json(self, write_file) -> None:
        with pytest.raises(json.JSONDecodeError):
            JsonDataReader().read(write_file('{"Сидоров Иван": '))

    def test_read_missing_file(self, tmpdir) -> None:
        with pytest.raises(FileNotFoundError):
            JsonDataReader().read(str(tmpdir.join("no_such_file.json")))
