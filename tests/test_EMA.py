#!/usr/bin/python3

import unittest
from bot.analysis import Analysis


class TestEMA(unittest.TestCase):
    # results source : https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:moving_averages
    # I didn't success to compute EMA with the Pandas library
    def test_EMA_fixed_values(self):
        random_numbers = [22.27, 22.19, 22.08, 22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29]
        mean = Analysis.SMA(random_numbers)
        self.assertTrue((round(mean, 2) == 22.22))
        random_numbers = [22.19, 22.08, 22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15]
        mean = Analysis.EMA(random_numbers, mean)
        self.assertTrue((round(mean, 2) == 22.21))
        random_numbers = [22.08, 22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39]
        mean = Analysis.EMA(random_numbers, mean)
        self.assertTrue((round(mean, 2) == 22.24))
        random_numbers = [22.17, 22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39, 22.38]
        mean = Analysis.EMA(random_numbers, mean)
        self.assertTrue((round(mean, 2) == 22.27))
        random_numbers = [22.18, 22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61]
        mean = Analysis.EMA(random_numbers, mean)
        self.assertTrue((round(mean, 2) == 22.33))
        random_numbers = [22.13, 22.23, 22.43, 22.24, 22.29, 22.15, 22.39, 22.38, 22.61, 23.36]
        mean = Analysis.EMA(random_numbers, mean)
        self.assertTrue((round(mean, 2) == 22.52))


if __name__ == '__main__':
    unittest.main()
