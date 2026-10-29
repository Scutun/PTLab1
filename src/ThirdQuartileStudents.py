# -*- coding: utf-8 -*-
import math

RatingType = dict[str, float]


class ThirdQuartileStudents:
    """Поиск студентов, чей рейтинг попадает в третью квартиль.

    Отсортированное по возрастанию распределение рейтингов делится
    квартилями Q1, Q2 (медиана) и Q3 на четыре интервала:
        1-я квартиль: [min; Q1]
        2-я квартиль: (Q1; Q2]
        3-я квартиль: (Q2; Q3]
        4-я квартиль: (Q3; max]
    Квантили вычисляются с линейной интерполяцией (как numpy.quantile
    по умолчанию и statistics.quantiles(method='inclusive')).
    """

    def __init__(self, rating: RatingType) -> None:
        self.rating: RatingType = rating
        self.q2: float = 0.0
        self.q3: float = 0.0

    @staticmethod
    def quantile(values: list[float], p: float) -> float:
        if not values:
            raise ValueError("Нельзя вычислить квантиль пустой выборки")
        if not 0.0 <= p <= 1.0:
            raise ValueError("Уровень квантиля должен лежать в [0; 1]")
        ordered = sorted(values)
        position = (len(ordered) - 1) * p
        lower = math.floor(position)
        upper = math.ceil(position)
        fraction = position - lower
        return ordered[lower] + fraction * (ordered[upper] - ordered[lower])

    def calc(self) -> RatingType:
        if not self.rating:
            return {}
        values = list(self.rating.values())
        self.q2 = self.quantile(values, 0.5)
        self.q3 = self.quantile(values, 0.75)
        result = {name: score for name, score in self.rating.items()
                  if self.q2 < score <= self.q3}
        return dict(sorted(result.items(),
                           key=lambda item: item[1], reverse=True))
