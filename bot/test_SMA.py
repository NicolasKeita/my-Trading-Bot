#!/usr/bin/python3

import unittest
from analysis import Analysis
from bot import Bot
from currencyEnum import CurrencyEnum
from io import StringIO
import sys
import pandas as pd

TEST_SMA_INPUT_FILE = "test_SMA_input.txt"


# TODO : generate a array of random nbr instead of reading the file / or do both
class TestSMA(unittest.TestCase):
    def test_SMA20(self):
        f = open(TEST_SMA_INPUT_FILE, "r")
        sys.stdin = StringIO(f.read())
        f.close()
        b = Bot()
        b.run()
        mean = Analysis.SMA(b.get_selected_candles(CurrencyEnum.USDT_ETH)[:20])
        self.assertTrue(mean == 1)


if __name__ == '__main__':
    unittest.main()

