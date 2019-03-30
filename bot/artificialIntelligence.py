class ArtificialIntelligence:
    def __init__(self):
        self.tmp = 0

    def decide_action(self, list_of_three_candles, stockpile):
        self.tmp += 1
        if self.tmp >= 10:
            return "pass"
        else:
            if len(list_of_three_candles) == 0:
                return "pass"
            candle = self.select_last_candle(list_of_three_candles, "USDT_ETH")
            amount_i_want_to_sell = (stockpile.USDT / 2) / candle.close
            return "buy USDT_ETH " + str(amount_i_want_to_sell)

    @staticmethod
    def select_last_candle(list_of_three_candles, pair):
        three_candles = list_of_three_candles[-1]
        for candle in three_candles:
            if candle.pair == pair:
                return candle
