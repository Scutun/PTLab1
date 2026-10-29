# -*- coding: utf-8 -*-
import json

from Types import DataType
from DataReader import DataReader


class JsonDataReader(DataReader):
    """Чтение данных о студентах из файла формата JSON.

    Ожидаемая структура файла:
    {
        "Иванов Иван Иванович": {"математика": 80, "химия": 91},
        "Петров Петр Петрович": {"физика": 76}
    }
    """

    MIN_SCORE: int = 0
    MAX_SCORE: int = 100

    def __init__(self) -> None:
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            raw_data = json.load(file)
        if not isinstance(raw_data, dict):
            raise ValueError("Корневой элемент JSON должен быть объектом")
        self.students = {}
        for name, subjects in raw_data.items():
            if not isinstance(subjects, dict):
                raise ValueError(
                    f"Оценки студента '{name}' должны быть объектом")
            self.students[name] = [
                (subject, self._check_score(name, subject, score))
                for subject, score in subjects.items()
            ]
        return self.students

    def _check_score(self, name: str, subject: str, score) -> int:
        # bool является подклассом int, поэтому исключаем его явно
        if isinstance(score, bool) or not isinstance(score, int):
            raise ValueError(
                f"Балл '{subject}' у '{name}' должен быть целым числом")
        if not self.MIN_SCORE <= score <= self.MAX_SCORE:
            raise ValueError(
                f"Балл '{subject}' у '{name}' вне диапазона "
                f"{self.MIN_SCORE}..{self.MAX_SCORE}")
        return score
