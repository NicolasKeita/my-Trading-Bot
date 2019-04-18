from bot.indicatorSet import IndicatorSet
from bot.analysis import Analysis
from bot.candle import Candle


class DataSet:
    def __init__(self):
        self.USDT_ETH = IndicatorSet()
        self.USDT_BTC = IndicatorSet()
        self.BTC_ETH = IndicatorSet()

    def feed(self, all_candles):
        self.__feed_SMA_arrays_and_EMA_arrays(all_candles)
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
            if len(all_candles) <= 26:
                SMA_26, EMA_26 = self.__update_SMA_EMA_first_time(all_candles, 26, "USDT_ETH")
            else:
                SMA_26, EMA_26 = self.__update_SMA_EMA(all_candles, 26, "USDT_ETH", self.USDT_ETH.EMA_26[-1])
            self.USDT_ETH.SMA_26.append(SMA_26)
            self.USDT_ETH.EMA_26.append(EMA_26)
            if len(all_candles) <= 40:
                SMA_40, EMA_40 = self.__update_SMA_EMA_first_time(all_candles, 40, "USDT_ETH")
            else:
                SMA_40, EMA_40 = self.__update_SMA_EMA(all_candles, 40, "USDT_ETH", self.USDT_ETH.EMA_40[-1])
            self.USDT_ETH.SMA_40.append(SMA_40)
            self.USDT_ETH.EMA_40.append(EMA_40)
            if len(all_candles) <= 80:
                SMA_80, EMA_80 = self.__update_SMA_EMA_first_time(all_candles, 80, "USDT_ETH")
            else:
                SMA_80, EMA_80 = self.__update_SMA_EMA(all_candles, 80, "USDT_ETH", self.USDT_ETH.EMA_80[-1])
            self.USDT_ETH.SMA_80.append(SMA_80)
            self.USDT_ETH.EMA_80.append(EMA_80)
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
