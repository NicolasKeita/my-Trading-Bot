from bot.candle import Candle


class RSI:
    def __init__(self):
        self.RSI_previous_average_gain = 0.0
        self.RSI_previous_average_loss = 0.0
        self.pre_buy_indicator = False
        self.pre_sell_indicator = False
        self.RSI = []
        self.buy_indicator = False
        self.sell_indicator = False

    def feed(self, all_candles, last_10_candles):
        if len(all_candles) < 10:
            return
        last_10_closing_prices = Candle.select_closing_prices(last_10_candles)
        if len(all_candles) == 10:
            gains = 0
            losses = 0
            for x in range(1, 10):
                delta = last_10_closing_prices[x] - last_10_closing_prices[x - 1]
                if delta < 0:
                    losses += abs(delta)
                else:
                    gains += delta
            self.RSI_previous_average_gain = gains / 10
            self.RSI_previous_average_loss = losses / 10
        else:
            delta = last_10_closing_prices[-1] - last_10_closing_prices[-2]
            current_gain = 0
            current_loss = 0
            if delta < 0:
                current_loss = abs(delta)
            else:
                current_gain = delta
            self.RSI_previous_average_gain = (self.RSI_previous_average_gain * 9 + current_gain) / 10
            self.RSI_previous_average_loss = (self.RSI_previous_average_loss * 9 + current_loss) / 10
            RS = self.RSI_previous_average_gain / self.RSI_previous_average_loss
            self.RSI.append(100 - 100 / (1 + RS))
            self.__update_RSI_indicator()

    def __update_RSI_indicator(self):
        self.buy_indicator = False
        self.sell_indicator = False
        if self.RSI[-1] > 70:
            self.pre_sell_indicator = True
        elif self.RSI[-1] < 30:
            self.pre_buy_indicator = True
        if self.pre_sell_indicator is True and self.RSI[-1] < 70:
            self.pre_sell_indicator = False
            self.sell_indicator = True
        elif self.pre_buy_indicator is True and self.RSI[-1] > 30:
            self.pre_buy_indicator = False
            self.buy_indicator = True
