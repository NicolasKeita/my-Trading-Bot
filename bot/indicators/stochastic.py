from bot.candle import Candle
from bot.indicators.SMA import SMA


class Stochastic:
    def __init__(self):
        self.stochastic_K = []
        self.stochastic_D = []
        self.buy_indicator = False
        self.sell_indicator = False
        self.oversold = False
        self.overbought = False

    def feed(self, last_14_candles):
        last_5_candles = last_14_candles[-5:]
        last_5_low = Candle.select_low(last_5_candles)
        last_5_high = Candle.select_high(last_5_candles)
        last_closing_price = last_5_candles[-1].close
        self.stochastic_K.append(100 * ((last_closing_price - min(last_5_low)) /
                                        (max(last_5_high) - min(last_5_low))))
        if len(self.stochastic_K) >= 3:
            self.stochastic_D.append(SMA.SMA(self.stochastic_K[-3:]))
            self.__update_stochastics_indicators()

    def __update_stochastics_indicators(self):
        self.buy_indicator = False
        self.sell_indicator = False
        if self.stochastic_D[-1] > 86:
            self.overbought = True
        elif self.stochastic_D[-1] < 20:
            self.oversold = True
        if self.overbought is True and self.stochastic_D[-1] < 86:
            self.overbought = False
            self.sell_indicator = True
        elif self.oversold is True and self.stochastic_D[-1] > 20:
            self.oversold = False
            self.buy_indicator = True
