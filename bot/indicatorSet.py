from enum import IntEnum, unique
from bot.indicators.SMA import SMA
from bot.indicators.EMA import EMA
from bot.indicators.MACD import MACD
from bot.indicators.bollingerBands import BollingerBands
from bot.indicators.stochastic import Stochastic
from bot.indicators.RSI import RSI
from bot.candle import Candle
import sys


class IndicatorSet:
    def __init__(self, pair_currency):
        self.pair = pair_currency
        self.SMA = SMA()
        self.EMA = EMA()
        self.standard_deviation = []
        self.MACD = MACD()
        self.BB = BollingerBands()
        self.stochastic = Stochastic()
        self.RSI = RSI()
        self.trend = Trend.CONSOLIDATION
        '''
        self.SMA_12 = []
        self.SMA_20 = []
        self.SMA_26 = []
        self.SMA_80 = []
        self.SMA_85 = []
        self.SMA_90 = []
        self.SMA_160 = []
        self.EMA_12 = []
        self.EMA_20 = []
        self.EMA_26 = []
        self.EMA_80 = []
        self.EMA_85 = []
        self.EMA_90 = []
        self.EMA_160 = []
        '''
        #self.MACD = []
        #self.MACD_signal = []
        #self.MACD_buy_indicator = False
        #self.MACD_sell_indicator = False
        #self.BBW = []
        #self.BB_indicator = False
        #self.stochastic_K = []
        #self.stochastic_D = []
        #self.stochastic_buy_indicator = False
        #self.stochastic_sell_indicator = False
        #self.RSI = []
        #self.RSI_buy_indicator = False
        #self.RSI_sell_indicator = False

    def feed(self, all_candles):
        self.__feed_SMA_arrays_and_EMA_arrays(all_candles)
        self.__define_trend(all_candles)
        self.MACD.feed(all_candles, self.EMA)
        self.__update_standard_deviation(all_candles)
        if len(all_candles) >= 10:
            last_10_candles = Candle.select_last_candles(all_candles, self.pair, 10)
            self.stochastic.feed(all_candles, last_10_candles)
            self.RSI.feed(all_candles, last_10_candles)
        if len(self.standard_deviation) >= 1 and len(self.SMA.SMA_20) >= 1:
            self.BB.feed(all_candles, self.SMA.SMA_20[-1], self.standard_deviation[-1])

    def __update_standard_deviation(self, all_candles):
        if len(all_candles) < 20:
            return
        last_20_candles = Candle.select_last_candles(all_candles, self.pair, 20)
        last_20_closing_prices = Candle.select_closing_prices(last_20_candles)
        from numpy import std
        self.standard_deviation.append(std(last_20_closing_prices))

    def __feed_SMA_arrays_and_EMA_arrays(self, all_candles):
        try:
            if len(all_candles) <= 12:
                SMA_12, EMA_12 = self.__update_SMA_EMA_first_time(all_candles, 12)
            else:
                SMA_12, EMA_12 = self.__update_SMA_EMA(all_candles, 12, self.EMA.EMA_12[-1])
            self.SMA.SMA_12.append(SMA_12)
            self.EMA.EMA_12.append(EMA_12)
            if len(all_candles) <= 20:
                SMA_20, EMA_20 = self.__update_SMA_EMA_first_time(all_candles, 20)
            else:
                SMA_20, EMA_20 = self.__update_SMA_EMA(all_candles, 20, self.EMA.EMA_20[-1])
            self.SMA.SMA_20.append(SMA_20)
            self.EMA.EMA_20.append(EMA_20)
            if len(all_candles) <= 26:
                SMA_26, EMA_26 = self.__update_SMA_EMA_first_time(all_candles, 26)
            else:
                SMA_26, EMA_26 = self.__update_SMA_EMA(all_candles, 26, self.EMA.EMA_26[-1])
            self.SMA.SMA_26.append(SMA_26)
            self.EMA.EMA_26.append(EMA_26)
            if len(all_candles) <= 80:
                SMA_80, EMA_80 = self.__update_SMA_EMA_first_time(all_candles, 80)
            else:
                SMA_80, EMA_80 = self.__update_SMA_EMA(all_candles, 80, self.EMA.EMA_80[-1])
            self.SMA.SMA_80.append(SMA_80)
            self.EMA.EMA_80.append(EMA_80)
            if len(all_candles) <= 85:
                SMA_85, EMA_85 = self.__update_SMA_EMA_first_time(all_candles, 85)
            else:
                SMA_85, EMA_85 = self.__update_SMA_EMA(all_candles, 85, self.EMA.EMA_85[-1])
            self.SMA.SMA_85.append(SMA_85)
            self.EMA.EMA_85.append(EMA_85)
            if len(all_candles) <= 90:
                SMA_90, EMA_90 = self.__update_SMA_EMA_first_time(all_candles, 90)
            else:
                SMA_90, EMA_90 = self.__update_SMA_EMA(all_candles, 90, self.EMA.EMA_90[-1])
            self.SMA.SMA_90.append(SMA_90)
            self.EMA.EMA_90.append(EMA_90)
            if len(all_candles) <= 160:
                SMA_160, EMA_160 = self.__update_SMA_EMA_first_time(all_candles, 160)
            else:
                SMA_160, EMA_160 = self.__update_SMA_EMA(all_candles, 160, self.EMA.EMA_160[-1])
            self.SMA.SMA_160.append(SMA_160)
            self.EMA.EMA_160.append(EMA_160)
        except AverageComputationTooEarly:
            pass

    def __update_SMA_EMA_first_time(self, all_candles, period):
        if len(all_candles) < period:
            raise AverageComputationTooEarly
        if len(all_candles) == period:
            last_candles = Candle.select_last_candles(all_candles, self.pair, period)
            SMA = self.SMA.SMA(Candle.select_closing_prices(last_candles))
            return SMA, SMA

    def __update_SMA_EMA(self, all_candles, period, previous_EMA):
        if len(all_candles) > period:
            last_candles = Candle.select_last_candles(all_candles, self.pair, period)
            SMA = self.SMA.SMA(Candle.select_closing_prices(last_candles))
            EMA = self.EMA.EMA(Candle.select_closing_prices(last_candles), previous_EMA)
            return SMA, EMA

    def __define_trend(self, all_candles):
        if len(all_candles) < 85:
            return
        last_candle = Candle.select_last_candles(all_candles, self.pair, 1)[0]
        if last_candle.close < self.EMA.EMA_85[-1]:
            self.trend = Trend.DOWNWARD
        else:
            self.trend = Trend.UPWARD


class AverageComputationTooEarly(Exception):
    pass

@unique
class Trend(IntEnum):
    UPWARD = 1
    DOWNWARD = 2
    CONSOLIDATION = 3
