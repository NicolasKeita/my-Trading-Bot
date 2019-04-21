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
    def select_closing_prices(candle_list):
        closing_prices = []
        for candle in candle_list:
            closing_prices.append(candle.close)
        return closing_prices

    @staticmethod
    def select_dates(candle_list):
        dates = []
        for candle in candle_list:
            dates.append(candle.date)
        return dates

    @staticmethod
    def select_high(candle_list):
        high = []
        for candle in candle_list:
            high.append(candle.high)
        return high

    @staticmethod
    def select_low(candle_list):
        low = []
        for candle in candle_list:
            low.append(candle.low)
        return low
