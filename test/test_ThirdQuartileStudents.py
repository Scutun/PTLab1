# -*- coding: utf-8 -*-
import pytest
from src.ThirdQuartileStudents import ThirdQuartileStudents

RatingsType = dict[str, float]


class TestThirdQuartileStudents:
    @pytest.fixture()
    def rating(self) -> RatingsType:
        # рейтинги студентов из data/data.json
        return {
            "Иванов Иван Иванович": 82.0,
            "Петров Петр Петрович": 83.6667,
            "Сидорова Анна Сергеевна": 97.6667,
            "Кузнецов Дмитрий Олегович": 65.3333,
            "Смирнова Елена Викторовна": 89.0,
            "Попов Артём Игоревич": 65.0,
            "Волкова Мария Андреевна": 87.0,
            "Новиков Сергей Павлович": 78.6667
        }

    def test_init(self, rating: RatingsType) -> None:
        calc = ThirdQuartileStudents(rating)
        assert calc.rating == rating
        assert calc.q2 == 0.0 and calc.q3 == 0.0

    @pytest.mark.parametrize("values, p, expected", [
        ([1, 2, 3, 4], 0.5, 2.5),
        ([1, 2, 3, 4], 0.75, 3.25),
        ([4, 1, 3, 2], 0.75, 3.25),
        ([1, 2, 3, 4], 0.0, 1.0),
        ([1, 2, 3, 4], 1.0, 4.0),
        ([1, 2, 3, 4, 5], 0.5, 3.0),
        ([5], 0.75, 5.0),
    ])
    def test_quantile(self, values: list[float], p: float,
                      expected: float) -> None:
        assert ThirdQuartileStudents.quantile(values, p) == \
            pytest.approx(expected)

    def test_quantile_empty(self) -> None:
        with pytest.raises(ValueError):
            ThirdQuartileStudents.quantile([], 0.5)

    @pytest.mark.parametrize("p", [-0.1, 1.5])
    def test_quantile_wrong_level(self, p: float) -> None:
        with pytest.raises(ValueError):
            ThirdQuartileStudents.quantile([1, 2, 3], p)

    def test_calc(self, rating: RatingsType) -> None:
        calc = ThirdQuartileStudents(rating)
        result = calc.calc()
        assert calc.q2 == pytest.approx(82.8333, abs=0.001)
        assert calc.q3 == pytest.approx(87.5, abs=0.001)
        assert result == {
            "Волкова Мария Андреевна": 87.0,
            "Петров Петр Петрович": 83.6667
        }

    def test_calc_sorted_descending(self, rating: RatingsType) -> None:
        scores = list(ThirdQuartileStudents(rating).calc().values())
        assert scores == sorted(scores, reverse=True)

    def test_calc_boundaries(self) -> None:
        # Q2 = 3, Q3 = 4: граница Q2 не входит, граница Q3 входит
        rating = {"A": 1.0, "B": 2.0, "C": 3.0, "D": 4.0, "E": 5.0}
        assert ThirdQuartileStudents(rating).calc() == {"D": 4.0}

    def test_calc_empty(self) -> None:
        assert ThirdQuartileStudents({}).calc() == {}

    def test_calc_one_student(self) -> None:
        assert ThirdQuartileStudents({"A": 90.0}).calc() == {}

    def test_calc_equal_ratings(self) -> None:
        rating = {"A": 80.0, "B": 80.0, "C": 80.0}
        assert ThirdQuartileStudents(rating).calc() == {}
