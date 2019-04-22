class BollingerBands:
    def __init__(self):
        self.BBW = []
        self.BB_indicator = False

    def feed(self, all_candles, last_SMA, last_standard_deviation):
        if len(all_candles) < 20:
            return
        upper_band = last_SMA + 2 * last_standard_deviation
        lower_band = last_SMA - 2 * last_standard_deviation
        self.BBW.append((upper_band - lower_band) / last_SMA)
        if len(self.BBW) >= 2:
            self.__update_bollinger_band_indicator()

    def __update_bollinger_band_indicator(self):
        self.BB_indicator = False
        if self.BBW[-2] < self.BBW[-1]:
            self.BB_indicator = True
