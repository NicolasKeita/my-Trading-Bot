from bot.analysis import Analysis
import sys


class ArtificialIntelligence:
    def __init__(self):
        self.SMA_12_USDT_ETH = []
        self.SMA_26_USDT_ETH = []
        self.SMA_40_USDT_ETH = []
        self.SMA_80_USDT_ETH = []
        self.SMA_160_USDT_ETH = []
        self.EMA_12_USDT_ETH = []
        self.EMA_26_USDT_ETH = []
        self.EMA_40_USDT_ETH = []
        self.EMA_80_USDT_ETH = []
        self.EMA_160_USDT_ETH = []
        self.MACD_USDT_ETH = []
        self.MACD_signal_USDT_ETH = []
        self.MACD_buy_indicator_USDT_ETH = False
        self.MACD_sell_indicator_USDT_ETH = False

    def update_stats(self, all_candles):
        self.__update_SMA_arrays_and_EMA_arrays(all_candles)
        if len(all_candles) >= 26:
            self.__update_MACD_arrays(all_candles)
            if len(all_candles) > 26:
                self.__update_MACD_indicators()

    def decide_action(self, all_candles, current_stockpile, bot_settings):
        if len(all_candles) == 0:
            return "pass"
        if self.MACD_buy_indicator_USDT_ETH == True:
            price_one_eth = self.__select_last_candles(all_candles, "USDT_ETH", 1)[0].close
            amount_i_want_to_buy = self.__percent(current_stockpile.USDT / price_one_eth,
                                                  bot_settings.transaction_fee_percent)
            return "buy USDT_ETH " + str(amount_i_want_to_buy)
        elif self.MACD_sell_indicator_USDT_ETH == True:
            amount_i_want_to_sell = current_stockpile.ETH
            return "sell USDT_ETH " + str(amount_i_want_to_sell)
        return "pass"

    def __update_MACD_indicators(self):
        self.MACD_buy_indicator_USDT_ETH = False
        self.MACD_sell_indicator_USDT_ETH = False
        if self.MACD_USDT_ETH[-2] < self.MACD_signal_USDT_ETH[-2] \
                and self.MACD_USDT_ETH[-1] > self.MACD_signal_USDT_ETH[-1]:
            self.MACD_buy_indicator_USDT_ETH = True
        elif self.MACD_USDT_ETH[-2] > self.MACD_signal_USDT_ETH[-2] \
                and self.MACD_USDT_ETH[-1] < self.MACD_signal_USDT_ETH[-1]:
            self.MACD_sell_indicator_USDT_ETH = True

    def __update_MACD_arrays(self, all_candles):
        self.MACD_USDT_ETH.append(abs(self.EMA_12_USDT_ETH[-1] - self.EMA_26_USDT_ETH[-1]))
        if len(all_candles) == 26:
            EMA_9 = Analysis.SMA(self.MACD_USDT_ETH[:-9])
            self.MACD_signal_USDT_ETH.append(EMA_9)
        elif len(all_candles) > 26:
            EMA_9 = Analysis.EMA(self.MACD_USDT_ETH[-9:], self.MACD_signal_USDT_ETH[-1])
            self.MACD_signal_USDT_ETH.append(EMA_9)

    def __update_SMA_arrays_and_EMA_arrays(self, all_candles):
        try:
            if len(all_candles) <= 12:
                SMA_12, EMA_12 = self.__update_SMA_EMA_first_time(all_candles, 12, "USDT_ETH")
            else:
                SMA_12, EMA_12 = self.__update_SMA_EMA(all_candles, 12, "USDT_ETH", self.EMA_12_USDT_ETH[-1])
            self.SMA_12_USDT_ETH.append(SMA_12)
            self.EMA_12_USDT_ETH.append(EMA_12)
            if len(all_candles) <= 26:
                SMA_26, EMA_26 = self.__update_SMA_EMA_first_time(all_candles, 26, "USDT_ETH")
            else:
                SMA_26, EMA_26 = self.__update_SMA_EMA(all_candles, 26, "USDT_ETH", self.EMA_26_USDT_ETH[-1])
            self.SMA_26_USDT_ETH.append(SMA_26)
            self.EMA_26_USDT_ETH.append(EMA_26)
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

    @staticmethod
    def __select_last_candles(all_candles, pair, number_of_candles):
        last_candles = []
        last_three_candles = all_candles[-number_of_candles:]
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

    @staticmethod
    def __percent(nbr, percentage):
        return nbr * (1 - percentage / 100)


class AverageComputationTooEarly(Exception):
    pass
