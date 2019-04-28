from bot.candle import Candle


class RSI:
    def __init__(self):
        self.RSI_previous_average_gain = 0.0
        self.RSI_previous_average_loss = 0.0
        self.oversold = False
        self.overbought = False
        self.RSI = []
        self.buy_indicator = False
        self.sell_indicator = False
        self.overbought = False
        self.oversold = False

    def feed(self, all_candles, last_14_candles):
        if len(all_candles) < 14:
            return
        last_14_closing_prices = Candle.select_closing_prices(last_14_candles)
        if len(all_candles) == 14:
            gains = 0
            losses = 0
            for x in range(1, 14):
                delta = last_14_closing_prices[x] - last_14_closing_prices[x - 1]
                if delta < 0:
                    losses += abs(delta)
                else:
                    gains += delta
            self.RSI_previous_average_gain = gains / 14
            self.RSI_previous_average_loss = losses / 14
        else:
            delta = last_14_closing_prices[-1] - last_14_closing_prices[-2]
            current_gain = 0
            current_loss = 0
            if delta < 0:
                current_loss = abs(delta)
            else:
                current_gain = delta
            self.RSI_previous_average_gain = (self.RSI_previous_average_gain * 13 + current_gain) / 14
            self.RSI_previous_average_loss = (self.RSI_previous_average_loss * 13 + current_loss) / 14
            RS = self.RSI_previous_average_gain / self.RSI_previous_average_loss
            self.RSI.append(100 - 100 / (1 + RS))
            self.__update_RSI_indicator()

    def __update_RSI_indicator(self):
        self.buy_indicator = False
        self.sell_indicator = False
        if self.RSI[-1] > 70:
            self.overbought = True
        elif self.RSI[-1] < 30:
            self.oversold = True
        if self.overbought is True and self.RSI[-1] < 71:
            self.overbought = False
            self.sell_indicator = True
        elif self.oversold is True and self.RSI[-1] > 30:
            self.oversold = False
            self.buy_indicator = True
