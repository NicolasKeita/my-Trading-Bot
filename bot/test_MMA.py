#!/usr/bin/python3

import unittest
from analysis import Analysis


class TestMMA(unittest.TestCase):
    def test_MMA20(self):
        mean = Analysis.MMA20(all_candles, USDT_ETH)
        self.assertTrue(mean == 1)


if __name__ == '__main__':
    unittest.main()

