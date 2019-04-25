from bot.candle import Candle
from bot.indicators.SMA import SMA


class Stochastic:
    def __init__(self):
        self.stochastic_K = []
        self.stochastic_D = []
        self.buy_indicator = False
        self.sell_indicator = False
        self.pre_buy_indicator = False
        self.pre_sell_indicator = False

    def feed(self, all_candles, last_14_candles):
        if len(all_candles) < 14:
            return
        last_14_low = Candle.select_low(last_14_candles)
        last_14_high = Candle.select_high(last_14_candles)
        last_closing_price = last_14_candles[-1].close
        self.stochastic_K.append(100 * ((last_closing_price - min(last_14_low)) /
                                        (max(last_14_high) - min(last_14_low))))
        if len(self.stochastic_K) >= 5:
            self.stochastic_D.append(SMA.SMA(self.stochastic_K[-5:]))
            self.__update_stochastics_indicators()

    def __update_stochastics_indicators(self):
        self.buy_indicator = False
        self.sell_indicator = False
        if self.stochastic_D[-1] > 80:
            self.pre_sell_indicator = True
        elif self.stochastic_D[-1] < 20:
            self.pre_buy_indicator = True
        if self.pre_sell_indicator is True and self.stochastic_D[-1] < 80:
            self.pre_sell_indicator = False
            self.sell_indicator = True
        elif self.pre_buy_indicator is True and self.stochastic_D[-1] > 20:
            self.pre_buy_indicator = False
            self.buy_indicator = True
