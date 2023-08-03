import numpy as np


class ChangePerYearProbability:
    def __init__(self, days: float, standard_deviation: float):
        self.price_hike_probablity = lambda: 1 / (
            365 / np.random.normal(days, standard_deviation)
        )

    def __call__(self):
        return self.price_hike_probablity()


class SalaryPercentageIncrease:
    def __init__(self, mean: float, standard_deviation: float):
        self.mean = mean
        self.standard_deviation = standard_deviation

    def __call__(self):
        return np.random.normal(loc=self.mean, scale=self.standard_deviation)
