class ArtificialIntelligence:
    def __init__(self):
        self.tmp = 0

    def decide_action(self, all_candles, current_stockpile):
        self.tmp += 1
        if self.tmp >= 10:
            return "pass"
        else:
            if len(all_candles) == 0:
                return "pass"
            candle = self.__select_last_candle(all_candles, "USDT_ETH")
            amount_i_want_to_sell = (current_stockpile.USDT / 2) / candle.close
            return "buy USDT_ETH " + str(amount_i_want_to_sell)

    @staticmethod
    def __select_last_candle(all_candles, pair):
        three_candles = all_candles[-1]
        for candle in three_candles:
            if candle.pair == pair:
                return candle
