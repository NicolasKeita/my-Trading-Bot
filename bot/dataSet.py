from bot.indicatorSet import IndicatorSet, Trend
from bot.analysis import Analysis
from bot.candle import Candle
import sys

class DataSet:
    def __init__(self):
        self.USDT_ETH = IndicatorSet()
        self.USDT_BTC = IndicatorSet()
        self.BTC_ETH = IndicatorSet()
        self.stochastics_buy_pre_indicator = False
        self.stochastics_sell_pre_indicator = False

    def feed(self, all_candles):
        self.__feed_SMA_arrays_and_EMA_arrays(all_candles)
        self.__define_trend(all_candles)
        self.__feed_MACD_arrays(all_candles)
        self.__feed_bollinger_arrays(all_candles)
        self.__feed_stochastics_arrays(all_candles)

    def __define_trend(self, all_candles):
        if len(all_candles) < 85:
            return
        last_candle = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[0]
        if last_candle.close < self.USDT_ETH.EMA_85[-1]:
            self.USDT_ETH.trend = Trend.DOWNWARD
        else:
            self.USDT_ETH.trend = Trend.UPWARD

    def __feed_stochastics_arrays(self, all_candles):
        if len(all_candles) < 10:
            return
        last_14_candles = Candle.select_last_candles(all_candles, "USDT_ETH", 10)
        last_14_low = Candle.select_low(last_14_candles)
        last_14_high = Candle.select_high(last_14_candles)
        last_closing_price = Candle.select_closing_prices(last_14_candles)[0]
        self.USDT_ETH.stochastic_K.append(100 * ((last_closing_price - min(last_14_low)) /
                                                 (max(last_14_high) - min(last_14_low))))
        if len(self.USDT_ETH.stochastic_K) >= 5:
            self.USDT_ETH.stochastic_D.append(Analysis.SMA(self.USDT_ETH.stochastic_K[-5:]))
            self.__update_stochastics_indicators()

    def __update_stochastics_indicators(self):
        self.USDT_ETH.stochastic_buy_indicator = False
        self.USDT_ETH.stochastic_sell_indicator = False
        if self.USDT_ETH.stochastic_D[-1] > 80:
            self.stochastics_sell_pre_indicator = True
        elif self.USDT_ETH.stochastic_D[-1] < 20:
            self.stochastics_buy_pre_indicator = True
        if self.stochastics_sell_pre_indicator is True and self.USDT_ETH.stochastic_D[-1] < 80:
            self.stochastics_sell_pre_indicator = False
            self.USDT_ETH.stochastic_sell_indicator = True
        elif self.stochastics_buy_pre_indicator is True and self.USDT_ETH.stochastic_D[-1] > 20:
            self.stochastics_buy_pre_indicator = False
            self.USDT_ETH.stochastic_buy_indicator = True

    def __feed_bollinger_arrays(self, all_candles):
        if len(all_candles) < 20:
            return
        last_20_candles = Candle.select_last_candles(all_candles, "USDT_ETH", 20)
        last_20_closing_prices = Candle.select_closing_prices(last_20_candles)
        from numpy import std
        self.USDT_ETH.standard_deviation.append(std(last_20_closing_prices))
        upper_band = self.USDT_ETH.SMA_20[-1] + 2 * self.USDT_ETH.standard_deviation[-1]
        lower_band = self.USDT_ETH.SMA_20[-1] - 2 * self.USDT_ETH.standard_deviation[-1]
        self.USDT_ETH.BBW.append((upper_band - lower_band) / self.USDT_ETH.SMA_20[-1])
        if len(all_candles) > 20:
            self.__update_bollinger_band_indicator()

    def __update_bollinger_band_indicator(self):
        self.USDT_ETH.BB_indicator = False
        if self.USDT_ETH.BBW[-2] < self.USDT_ETH.BBW[-1]:
            self.USDT_ETH.BB_indicator = True

    def __feed_MACD_arrays(self, all_candles):
        if len(all_candles) >= 26:
            self.__update_MACD_arrays(all_candles)
            if len(all_candles) > 26:
                self.__update_MACD_indicators()

    def __update_MACD_indicators(self):
        self.USDT_ETH.MACD_buy_indicator = False
        self.USDT_ETH.MACD_sell_indicator = False
        if len(self.USDT_ETH.MACD) >= 26 + 9:
            if self.USDT_ETH.MACD[-2] < self.USDT_ETH.MACD_signal[-2] \
                    and self.USDT_ETH.MACD[-1] > self.USDT_ETH.MACD_signal[-1]:
                self.USDT_ETH.MACD_buy_indicator = True
            elif self.USDT_ETH.MACD[-2] > self.USDT_ETH.MACD_signal[-2] \
                    and self.USDT_ETH.MACD[-1] < self.USDT_ETH.MACD_signal[-1]:
                self.USDT_ETH.MACD_sell_indicator = True

    def __update_MACD_arrays(self, all_candles):
        self.USDT_ETH.MACD.append(self.USDT_ETH.EMA_12[-1] - self.USDT_ETH.EMA_26[-1])
        if len(all_candles) == 26 + 9:
            EMA_9 = Analysis.SMA(self.USDT_ETH.MACD[:-9])
            self.USDT_ETH.MACD_signal.append(EMA_9)
        elif len(all_candles) > 26 + 9:
            EMA_9 = Analysis.EMA(self.USDT_ETH.MACD[-9:], self.USDT_ETH.MACD_signal[-1])
            self.USDT_ETH.MACD_signal.append(EMA_9)

    def __feed_SMA_arrays_and_EMA_arrays(self, all_candles):
        try:
            if len(all_candles) <= 12:
                SMA_12, EMA_12 = self.__update_SMA_EMA_first_time(all_candles, 12, "USDT_ETH")
            else:
                SMA_12, EMA_12 = self.__update_SMA_EMA(all_candles, 12, "USDT_ETH", self.USDT_ETH.EMA_12[-1])
            self.USDT_ETH.SMA_12.append(SMA_12)
            self.USDT_ETH.EMA_12.append(EMA_12)
            if len(all_candles) <= 20:
                SMA_20, EMA_20 = self.__update_SMA_EMA_first_time(all_candles, 20, "USDT_ETH")
            else:
                SMA_20, EMA_20 = self.__update_SMA_EMA(all_candles, 20, "USDT_ETH", self.USDT_ETH.EMA_20[-1])
            self.USDT_ETH.SMA_20.append(SMA_20)
            self.USDT_ETH.EMA_20.append(EMA_20)
            if len(all_candles) <= 26:
                SMA_26, EMA_26 = self.__update_SMA_EMA_first_time(all_candles, 26, "USDT_ETH")
            else:
                SMA_26, EMA_26 = self.__update_SMA_EMA(all_candles, 26, "USDT_ETH", self.USDT_ETH.EMA_26[-1])
            self.USDT_ETH.SMA_26.append(SMA_26)
            self.USDT_ETH.EMA_26.append(EMA_26)
            if len(all_candles) <= 80:
                SMA_80, EMA_80 = self.__update_SMA_EMA_first_time(all_candles, 80, "USDT_ETH")
            else:
                SMA_80, EMA_80 = self.__update_SMA_EMA(all_candles, 80, "USDT_ETH", self.USDT_ETH.EMA_80[-1])
            self.USDT_ETH.SMA_80.append(SMA_80)
            self.USDT_ETH.EMA_80.append(EMA_80)
            if len(all_candles) <= 85:
                SMA_85, EMA_85 = self.__update_SMA_EMA_first_time(all_candles, 85, "USDT_ETH")
            else:
                SMA_85, EMA_85 = self.__update_SMA_EMA(all_candles, 85, "USDT_ETH", self.USDT_ETH.EMA_85[-1])
            self.USDT_ETH.SMA_85.append(SMA_85)
            self.USDT_ETH.EMA_85.append(EMA_85)
            if len(all_candles) <= 90:
                SMA_90, EMA_90 = self.__update_SMA_EMA_first_time(all_candles, 90, "USDT_ETH")
            else:
                SMA_90, EMA_90 = self.__update_SMA_EMA(all_candles, 90, "USDT_ETH", self.USDT_ETH.EMA_90[-1])
            self.USDT_ETH.SMA_90.append(SMA_90)
            self.USDT_ETH.EMA_90.append(EMA_90)
            if len(all_candles) <= 160:
                SMA_160, EMA_160 = self.__update_SMA_EMA_first_time(all_candles, 160, "USDT_ETH")
            else:
                SMA_160, EMA_160 = self.__update_SMA_EMA(all_candles, 160, "USDT_ETH", self.USDT_ETH.EMA_160[-1])
            self.USDT_ETH.SMA_160.append(SMA_160)
            self.USDT_ETH.EMA_160.append(EMA_160)
        except AverageComputationTooEarly:
            pass

    def __update_SMA_EMA_first_time(self, all_candles, period, pair):
        if len(all_candles) < period:
            raise AverageComputationTooEarly
        if len(all_candles) == period:
            last_candles = Candle.select_last_candles(all_candles, pair, period)
            SMA = Analysis.SMA(Candle.select_closing_prices(last_candles))
            return SMA, SMA

    def __update_SMA_EMA(self, all_candles, period, pair, previous_EMA):
        if len(all_candles) > period:
            last_candles = Candle.select_last_candles(all_candles, pair, period)
            SMA = Analysis.SMA(Candle.select_closing_prices(last_candles))
            EMA = Analysis.EMA(Candle.select_closing_prices(last_candles), previous_EMA)
            return SMA, EMA


class AverageComputationTooEarly(Exception):
    pass
