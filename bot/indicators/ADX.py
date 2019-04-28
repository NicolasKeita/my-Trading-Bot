from bot.indicators.SMA import SMA
from decimal import *
import sys
from enum import IntEnum, unique

@unique
class Trend(IntEnum):
    UPWARD = 1
    DOWNWARD = 2
    CONSOLIDATION = 3

class ADX:
    def __init__(self):
        self.TR = []
        self.ATR = []
        self.DI_positive = []
        self.DI_negative = []
        self.DM_positive = []
        self.DM_negative = []
        self.DM_14_pos = []
        self.DM_14_neg = []
        self.smoothed_DM_positive = []
        self.smoothed_DM_negative = []
        self.DX = []
        self.ADX = []
        self.trend_strength = 0
        self.trend = Trend.CONSOLIDATION
        self.buy_authorized = True
        self.sell_authorized = True
        self.buy_indicator = False
        self.sell_indicator = False

    def feed(self, last_2_candles):
        getcontext().prec = 10
        self.__feed_ATR(last_2_candles[-1], last_2_candles[-2])
        self.__feed_ADX(last_2_candles[-1], last_2_candles[-2])
        self.__define_trend_strength()
        self.__update_trend()
        self.__update_authorizations()
        self.__update_indicators()

    def __update_indicators(self):
        if len(self.ADX) == 0:
            return
        self.buy_indicator = False
        self.sell_indicator = False
        if self.DI_positive[-2] > self.DI_negative[-2] and self.DI_positive[-1] <= self.DI_negative[-1] and self.ADX[-1] > 24:
            self.buy_indicator = True
        elif self.DI_positive[-2] <= self.DI_negative[-2] and self.DI_positive[-1] > self.DI_negative[-1] and self.ADX[-1] > 24:
            self.sell_indicator = True

    def __update_authorizations(self):
        if len(self.ADX) == 0:
            return
        self.buy_authorized = True
        self.sell_authorized = True
        if self.ADX[-1] < 25:
            self.buy_authorized = False
            self.sell_authorized = False
        if self.DI_positive[-1] > 26:
            self.sell_authorized = False
        if self.DI_negative[-1] > 26:
            self.buy_authorized = False

    def __define_trend_strength(self):
        if len(self.ADX) > 0:
            if self.ADX[-1] < 13.637:
                self.trend_strength = 0
            elif self.ADX[-1] < 25:
                self.trend_strength = 1
            elif self.ADX[-1] < 30:
                self.trend_strength = 2
            elif self.ADX[-1] < 35:
                self.trend_strength = 3
            elif self.ADX[-1] < 40:
                self.trend_strength = 4
            elif self.ADX[-1] < 45:
                self.trend_strength = 5
            elif self.ADX[-1] < 50:
                self.trend_strength = 6

    def __update_trend(self):
        if len(self.DI_positive) == 0:
            return
        if self.DI_positive[-1] > self.DI_negative[-1] + 5:
            self.trend = Trend.UPWARD
        elif self.DI_negative[-1] > self.DI_positive[-1] + 5:
            self.trend = Trend.DOWNWARD
        else:
            self.trend = Trend.CONSOLIDATION

    def __feed_ATR(self, current_candle, previous_candle):
        H_less_L = current_candle.high - current_candle.low
        if len(self.TR) >= 1:
            current_H_less_previous_close = abs(current_candle.high - previous_candle.close)
            current_low_less_previous_close = abs(current_candle.low - previous_candle.close)
        else:
            current_H_less_previous_close = 0
            current_low_less_previous_close = 0
        if (H_less_L >= current_H_less_previous_close) and (H_less_L >= current_low_less_previous_close):
            greatest = H_less_L
        elif (current_H_less_previous_close >= H_less_L) and (current_H_less_previous_close >= current_low_less_previous_close):
            greatest = current_H_less_previous_close
        else:
            greatest = current_low_less_previous_close
        self.TR.append(greatest)
        if len(self.TR) >= 14:
            if len(self.ATR) == 0:
                self.ATR.append(sum(self.TR[-14:]))
            else:
                self.ATR.append((14 - 1) / 14 * self.ATR[-1] + self.TR[-1])

    def __feed_ADX(self, current_candle, previous_candle):
        DM_pos = Decimal(current_candle.high) - Decimal(previous_candle.high)
        DM_neg = Decimal(previous_candle.low) - Decimal(current_candle.low)
        if DM_pos >= DM_neg:
            self.DM_positive.append(float(DM_pos))
            self.DM_negative.append(0)
        else:
            self.DM_negative.append(float(DM_neg))
            self.DM_positive.append(0)
        if len(self.DM_positive) >= 14:
            if len(self.DM_14_pos) == 0:
                self.DM_14_pos.append(sum(self.DM_positive[-14:]))
                self.DM_14_neg.append(sum(self.DM_negative[-14:]))
            else:
                self.DM_14_pos.append(((14 - 1) / 14) * self.DM_14_pos[-1] + self.DM_positive[-1])
                self.DM_14_neg.append(((14 - 1) / 14) * self.DM_14_neg[-1] + self.DM_negative[-1])
            self.DI_positive.append(100 * (self.DM_14_pos[-1] / self.ATR[-1]))
            self.DI_negative.append(100 * (self.DM_14_neg[-1] / self.ATR[-1]))
            self.DX.append(((abs(self.DI_positive[-1] - self.DI_negative[-1])) /
                           (abs(self.DI_positive[-1] + self.DI_negative[-1]))) * 100)
            if len(self.DX) == 14:
                self.ADX.append(SMA.SMA(self.DX[-14:]))
            elif len(self.DX) > 14:
                self.ADX.append(((self.ADX[-1] * 13) + self.DX[-1]) / 14)
