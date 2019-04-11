#!/usr/bin/python3

import unittest
from analysis import Analysis
from bot import Bot
from currencyEnum import CurrencyEnum
from io import StringIO
import sys
import pandas as pd
import numpy as np

TEST_SMA_INPUT_FILE = "test_SMA_input.txt"


class TestSMA(unittest.TestCase):
    def test_all_SMA(self):
        self.__test_SMA(20)
        self.__test_SMA(10)
        self.__test_SMA(1)
        self.__test_SMA(5)
        self.__test_SMA(40)
        self.__test_SMA(400)
        self.__test_SMA(1000)
        self.__test_SMA(5000)
        self.__test_SMA(10000)
        self.__test_SMA(100000)

    def __test_SMA(self, window):
        random_numbers = np.random.rand(window)
        mean = Analysis.SMA(random_numbers)
        r = pd.Series(random_numbers)
        panda_means = r.rolling(window=window).mean()
        panda_mean = panda_means.tolist()[window - 1]
        self.assertTrue(mean == panda_mean)

    # This test is not isolated. (Half of the program is also executed)
    # It takes real values from the file "test_SMA_input.txt"
    def test_SMA20(self):
        f = open(TEST_SMA_INPUT_FILE, "r")
        sys.stdin = StringIO(f.read())
        f.close()
        b = Bot()
        b.run()
        selected_candles = b.get_selected_candles(CurrencyEnum.USDT_ETH)[:20]
        closing_prices = []
        for candle in selected_candles:
            closing_prices.append(candle.close)
        mean = Analysis.SMA(closing_prices)
        r = pd.Series(closing_prices)
        panda_means = r.rolling(window=20).mean()
        panda_mean = panda_means.tolist()[19]
        self.assertTrue(mean == panda_mean)


if __name__ == '__main__':
    unittest.main()

