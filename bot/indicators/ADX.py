from bot.indicators.SMA import SMA
from bot.indicators.EMA import EMA

class ADX:
    def __init__(self):
        self.TR = []
        self.ATR = []
        self.DI_positive = []
        self.DI_negative = []
        self.DM_positive = []
        self.DM_negative = []
        self.smoothed_DM_positive = []
        self.smoothed_DM_negative = []
        self.DX = []
        self.ADX = []
        self.trend_strength = 0

    def feed(self, last_2_candles):
        self.__feed_ATR(last_2_candles[-1], last_2_candles[-2])
        self.__feed_ADX(last_2_candles[-1], last_2_candles[-2])
        self.__define_trend_strength()

    def __define_trend_strength(self):
        if len(self.ADX) > 0:
            if self.ADX[-1] < 25:
                self.trend_strength = 0
            elif self.ADX[-1] < 50:
                self.trend_strength = 1
            elif self.ADX[-1] < 75:
                self.trend_strength = 2

    def __feed_ATR(self, current_candle, previous_candle):
        H_less_L = current_candle.high - current_candle.low
        if len(self.TR) >= 1:
            current_H_less_previous_close = abs(current_candle.high - previous_candle.close)
            current_low_less_previous_close = abs(current_candle.low - previous_candle.close)
        else:
            current_H_less_previous_close = 0
            current_low_less_previous_close = 0
        self.TR.append(max(H_less_L, current_H_less_previous_close, current_low_less_previous_close))
        if len(self.TR) >= 14:
            if len(self.ATR) == 0:
                self.ATR.append(SMA.SMA(self.TR[-14:]))
            else:
                self.ATR.append((self.ATR[-1] * 13 + self.TR[-1]) / 14)

    def __feed_ADX(self, current_candle, previous_candle):
        self.DM_positive.append(max(current_candle.high - previous_candle.high, 0))
        self.DM_negative.append(max(previous_candle.low - current_candle.low, 0))
        if len(self.DM_positive) >= 14:
            if len(self.smoothed_DM_positive) == 0:
                self.smoothed_DM_positive.append(SMA.SMA(self.DM_positive[-14:]))
                self.smoothed_DM_negative.append(SMA.SMA(self.DM_negative[-14:]))
            else:
                self.smoothed_DM_positive.append(EMA.EMA(self.DM_positive[-14:], self.smoothed_DM_positive[-1]))
                self.smoothed_DM_negative.append(EMA.EMA(self.DM_negative[-14:], self.smoothed_DM_negative[-1]))
            self.DI_positive.append(100 * self.smoothed_DM_positive[-1] / self.ATR[-1])
            self.DI_negative.append(100 * self.smoothed_DM_negative[-1] / self.ATR[-1])
            self.DX.append(((abs(self.DI_positive[-1] - self.DI_negative[-1])) /
                           (abs(self.DI_positive[-1] + self.DI_negative[-1]))) * 100)
            if len(self.DX) == 14:
                self.ADX.append(SMA.SMA(self.DX[-14:]))
            elif len(self.DX) > 14:
                self.ADX.append(((self.ADX[-1] * 13) + self.DX[-1]) / 14)
