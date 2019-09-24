from bot.indicators.SMA import SMA


class MACD:
    def __init__(self):
        self.MACD = []
        self.MACD_signal = []
        self.buy_indicator = False
        self.sell_indicator = False

    def feed(self, number_of_candles, EMA):
        if number_of_candles >= 26:
            self.__update_MACD_arrays(number_of_candles, EMA)
            if number_of_candles > 26:
                self.__update_indicators()

    def __update_indicators(self):
        self.buy_indicator = False
        self.sell_indicator = False
        if len(self.MACD) >= 26 + 9:
            if self.MACD[-2] < self.MACD_signal[-2] \
                    and self.MACD[-1] > self.MACD_signal[-1]:
                self.buy_indicator = True
            elif self.MACD[-2] > self.MACD_signal[-2] \
                    and self.MACD[-1] < self.MACD_signal[-1]:
                self.sell_indicator = True

    def __update_MACD_arrays(self, number_of_candles, EMA):
        self.MACD.append(EMA.EMA_12[-1] - EMA.EMA_26[-1])
        if number_of_candles == 26 + 9:
            EMA_9 = SMA.SMA(self.MACD[:-9])
            self.MACD_signal.append(EMA_9)
        elif number_of_candles > 26 + 9:
            EMA_9 = EMA.EMA(self.MACD[-9:], self.MACD_signal[-1])
            self.MACD_signal.append(EMA_9)
