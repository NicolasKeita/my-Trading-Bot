from bot.analysis import Analysis
import sys
from contextlib import suppress


class ArtificialIntelligence:
    def __init__(self):
        self.SMA_10_USDT_ETH = []
        self.SMA_20_USDT_ETH = []
        self.SMA_40_USDT_ETH = []
        self.SMA_80_USDT_ETH = []
        self.SMA_160_USDT_ETH = []
        self.EMA_10_USDT_ETH = []
        self.EMA_20_USDT_ETH = []
        self.EMA_40_USDT_ETH = []
        self.EMA_80_USDT_ETH = []
        self.EMA_160_USDT_ETH = []
        self.tmp = 0

    def update_stats(self, all_candles):
        try:
            if len(all_candles) <= 10:
                SMA_10, EMA_10 = self.__update_SMA_EMA_first_time(all_candles, 10, "USDT_ETH")
            else:
                SMA_10, EMA_10 = self.__update_SMA_EMA(all_candles, 10, "USDT_ETH", self.EMA_10_USDT_ETH[-1])
            self.SMA_10_USDT_ETH.append(SMA_10)
            self.EMA_10_USDT_ETH.append(EMA_10)
            if len(all_candles) <= 20:
                SMA_20, EMA_20 = self.__update_SMA_EMA_first_time(all_candles, 20, "USDT_ETH")
            else:
                SMA_20, EMA_20 = self.__update_SMA_EMA(all_candles, 20, "USDT_ETH", self.EMA_20_USDT_ETH[-1])
            self.SMA_20_USDT_ETH.append(SMA_20)
            self.EMA_20_USDT_ETH.append(EMA_20)
            if len(all_candles) <= 40:
                SMA_40, EMA_40 = self.__update_SMA_EMA_first_time(all_candles, 40, "USDT_ETH")
            else:
                SMA_40, EMA_40 = self.__update_SMA_EMA(all_candles, 40, "USDT_ETH", self.EMA_40_USDT_ETH[-1])
            self.SMA_40_USDT_ETH.append(SMA_40)
            self.EMA_40_USDT_ETH.append(EMA_40)
            if len(all_candles) <= 80:
                SMA_80, EMA_80 = self.__update_SMA_EMA_first_time(all_candles, 80, "USDT_ETH")
            else:
                SMA_80, EMA_80 = self.__update_SMA_EMA(all_candles, 80, "USDT_ETH", self.EMA_80_USDT_ETH[-1])
            self.SMA_80_USDT_ETH.append(SMA_80)
            self.EMA_80_USDT_ETH.append(EMA_80)
            if len(all_candles) <= 160:
                SMA_160, EMA_160 = self.__update_SMA_EMA_first_time(all_candles, 160, "USDT_ETH")
            else:
                SMA_160, EMA_160 = self.__update_SMA_EMA(all_candles, 160, "USDT_ETH", self.EMA_160_USDT_ETH[-1])
            self.SMA_160_USDT_ETH.append(SMA_160)
            self.EMA_160_USDT_ETH.append(EMA_160)
        except AverageComputationTooEarly:
            pass

    def __update_SMA_EMA_first_time(self, all_candles, period, pair):
        if len(all_candles) < period:
            raise AverageComputationTooEarly
        if len(all_candles) == period:
            last_candles = self.__select_last_candles(all_candles, pair, period)
            SMA = Analysis.SMA(self.__select_closing_prices(last_candles))
            return SMA, SMA

    def __update_SMA_EMA(self, all_candles, period, pair, previous_EMA):
        if len(all_candles) > period:
            last_candles = self.__select_last_candles(all_candles, pair, period)
            SMA = Analysis.SMA(self.__select_closing_prices(last_candles))
            EMA = Analysis.EMA(self.__select_closing_prices(last_candles), previous_EMA)
            return SMA, EMA

    def decide_action(self, all_candles, current_stockpile):
        self.tmp += 1
        if self.tmp >= 10:
            return "pass"
        else:
            if len(all_candles) == 0:
                return "pass"
            candle = self.__select_last_candles(all_candles, "USDT_ETH", 1)[0]
            amount_i_want_to_sell = (current_stockpile.USDT / 2) / candle.close
            return "buy USDT_ETH " + str(amount_i_want_to_sell)

    @staticmethod
    def __select_last_candles(all_candles, pair, number_of_candles):
        last_candles = []
        last_three_candles = all_candles[:-number_of_candles]
        for three_candles in last_three_candles:
            for candle in three_candles:
                if candle.pair == pair:
                    last_candles.append(candle)
        return last_candles

    @staticmethod
    def __select_closing_prices(candles):
        closing_prices = []
        for candle in candles:
            closing_prices.append(candle.close)
        return closing_prices


class AverageComputationTooEarly(Exception):
    pass
