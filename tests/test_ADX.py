#!/usr/bin/python3

import unittest
import numpy as np
import pandas as pd
import logging
from bot.indicators.SMA import SMA
from bot.indicators.EMA import EMA
from bot.indicators.ADX import ADX
from bot.candle import Candle
import math
import sys


def truncate(f, n):
    return math.floor(f * 10 ** n) / 10 ** n


class TestADX(unittest.TestCase):
    # source values are from : https://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:average_directional_index_adx
    def test_ADX_fixed_values(self):
        adx = ADX()
        candle_1 = Candle("USDT_ETH", 30.20, 29.41, 29.87)
        candle_2 = Candle("USDT_ETH", 30.28, 29.32, 30.24)
        adx.feed([candle_1, candle_2])
        self.assertTrue(truncate(adx.TR[-1], 2) == 0.96)
        self.assertTrue(truncate(adx.DM_positive[-1], 2) == 0.00)
        self.assertTrue(truncate(adx.DM_negative[-1], 2) == 0.09)

        candle_3 = Candle("USDT_ETH", 30.45, 29.96, 30.10)
        adx.feed([candle_2, candle_3])
        self.assertTrue(truncate(adx.TR[-1], 2) == 0.48)
        self.assertTrue(round(adx.DM_positive[-1], 2) == 0.17)
        self.assertTrue(round(adx.DM_negative[-1], 2) == 0.00)

        candle_4 = Candle("USDT_ETH", 29.35, 28.74, 28.90)
        adx.feed([candle_3, candle_4])
        self.assertTrue(truncate(adx.TR[-1], 2) == 1.36)
        self.assertTrue(round(adx.DM_positive[-1], 2) == 0.00)
        self.assertTrue(round(adx.DM_negative[-1], 2) == 1.22)

        candle_5 = Candle("USDT_ETH", 29.35, 28.56, 28.92)
        adx.feed([candle_4, candle_5])
        self.assertTrue(truncate(adx.TR[-1], 2) == 0.79)
        self.assertTrue(round(adx.DM_positive[-1], 2) == 0.00)
        self.assertTrue(round(adx.DM_negative[-1], 2) == 0.18)

        candle_6 = Candle("USDT_ETH", 29.29, 28.41, 29.48)
        adx.feed([candle_5, candle_6])
        candle_7 = Candle("USDT_ETH", 28.83, 28.08, 28.56)
        adx.feed([candle_6, candle_7])
        candle_8 = Candle("USDT_ETH", 28.73, 27.43, 27.56)
        adx.feed([candle_7, candle_8])
        candle_9 = Candle("USDT_ETH", 28.67, 27.66, 28.47)
        adx.feed([candle_8, candle_9])
        candle_10 = Candle("USDT_ETH", 28.85, 27.83, 28.28)
        adx.feed([candle_9, candle_10])
        candle_11 = Candle("USDT_ETH", 28.64, 27.40, 27.49)
        adx.feed([candle_10, candle_11])
        candle_12 = Candle("USDT_ETH", 27.68, 27.09, 27.23)
        adx.feed([candle_11, candle_12])
        candle_13 = Candle("USDT_ETH", 27.21, 26.18, 26.35)
        adx.feed([candle_12, candle_13])
        candle_14 = Candle("USDT_ETH", 26.87, 26.13, 26.33)
        adx.feed([candle_13, candle_14])
        candle_15 = Candle("USDT_ETH", 27.41, 26.63, 27.03)
        adx.feed([candle_14, candle_15])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_16 = Candle("USDT_ETH", 26.94, 26.13, 26.22)
        adx.feed([candle_15, candle_16])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_17 = Candle("USDT_ETH", 26.52, 25.43, 26.01)
        adx.feed([candle_16, candle_17])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_18 = Candle("USDT_ETH", 26.52, 25.35, 25.46)
        adx.feed([candle_17, candle_18])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_19 = Candle("USDT_ETH", 27.09, 25.88, 27.03)
        adx.feed([candle_18, candle_19])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_20 = Candle("USDT_ETH", 27.69, 26.96, 27.45)
        adx.feed([candle_19, candle_20])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_21 = Candle("USDT_ETH", 27.69, 26.96, 28.36)
        adx.feed([candle_20, candle_21])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_22 = Candle("USDT_ETH", 28.53, 28.01, 28.43)
        adx.feed([candle_21, candle_22])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_23 = Candle("USDT_ETH", 28.67, 27.88, 27.95)
        adx.feed([candle_22, candle_23])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_24 = Candle("USDT_ETH", 29.01, 27.99, 29.01)
        adx.feed([candle_23, candle_24])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_25 = Candle("USDT_ETH", 29.87, 28.76, 29.38)
        adx.feed([candle_24, candle_25])
        #print("TR = ", adx.TR[-1], "DI_pos = ", adx.DI_positive[-1], "DX = ", adx.DX[-1], file=sys.stderr)
        candle_26 = Candle("USDT_ETH", 29.80, 29.14, 29.36)
        adx.feed([candle_25, candle_26])
        candle_27 = Candle("USDT_ETH", 29.75, 28.71, 28.91)
        adx.feed([candle_26, candle_27])
        candle_28 = Candle("USDT_ETH", 30.65, 28.93, 30.61)
        adx.feed([candle_27, candle_28])
        #print("DX = ", adx.DX[-1], "ADX = ", adx.ADX[-1], file=sys.stderr)


if __name__ == '__main__':
    unittest.main()