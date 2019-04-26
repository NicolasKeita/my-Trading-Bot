class BollingerBands:
    def __init__(self):
        self.BBW = []
        self.BB_indicator = False
        self.buy_indicator = False
        self.sell_indicator = False

    def feed(self, last_SMA, last_standard_deviation, last_close):
        upper_band = last_SMA + 2 * last_standard_deviation
        lower_band = last_SMA - 2 * last_standard_deviation
        self.BBW.append((upper_band - lower_band) / last_SMA)
        if len(self.BBW) >= 2:
            self.__update_bollinger_band_indicator(last_close, upper_band, lower_band)

    def __update_bollinger_band_indicator(self, last_close, upper_band, lower_band):
        self.BB_indicator = False
        self.buy_indicator = False
        self.sell_indicator = False
        if self.BBW[-2] < self.BBW[-1]:
            self.BB_indicator = True
        if last_close < lower_band:
            self.sell_indicator = True
        elif last_close > upper_band:
            self.buy_indicator = True
