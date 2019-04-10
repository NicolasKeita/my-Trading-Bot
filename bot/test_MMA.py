#!/usr/bin/python3

import unittest
from analysis import Analysis
from bot.bot import Bot
from currencyEnum import CurrencyEnum


class TestMMA(unittest.TestCase):
    def test_MMA20(self):
        b = Bot()
        b.run()
        mean = Analysis.MMA(b.get_selected_candles(CurrencyEnum.USDT_ETH)[:20])
        self.assertTrue(mean == 1)


if __name__ == '__main__':
    unittest.main()

