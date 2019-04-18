class Candle:
    def __init__(self, pair):
        self.pair = pair
        self.date = 0
        self.high = 0.0
        self.low = 0.0
        self.open = 0.0
        self.close = 0.0
        self.volume = 0.0

    @staticmethod
    def select_last_candles(all_candles, pair, number_of_candles):
        last_candles = []
        if number_of_candles == -1:
            last_three_candles = all_candles
        else:
            last_three_candles = all_candles[-number_of_candles:]
        for three_candles in last_three_candles:
            for candle in three_candles:
                if candle.pair == pair:
                    last_candles.append(candle)
        return last_candles

    @staticmethod
    def select_closing_prices(candles):
        closing_prices = []
        for candle in candles:
            closing_prices.append(candle.close)
        return closing_prices

    @staticmethod
    def select_dates(candles):
        dates = []
        for candle in candles:
            dates.append(candle.date)
        return dates
