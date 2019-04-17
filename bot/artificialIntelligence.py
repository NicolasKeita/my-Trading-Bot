from bot.analysis import Analysis


class ArtificialIntelligence:
    def __init__(self):
        self.SMA_10_USDT_ETH = []
        self.SMA_20_USDT_ETH = []
        self.SMA_40_USDT_ETH = []
        self.SMA_80_USDT_ETH = []
        self.SMA_160_USDT_ETH = []
        self.EMA_10_USDT_ETH = []
        self.EMA_20_USDT_ETH = []
        self.EMA_40_USDT_ETH = []
        self.EMA_80_USDT_ETH = []
        self.EMA_160_USDT_ETH = []
        self.tmp = 0

    def update_stats(self, all_candles):
        if len(all_candles) >= 10:
            self.SMA_10_USDT_ETH.append(Analysis.SMA(all_candles[:-10]))
        if len(all_candles) >= 20:
            self.SMA_20_USDT_ETH.append(Analysis.SMA(all_candles[:-20]))

    def decide_action(self, all_candles, current_stockpile):
        self.tmp += 1
        if self.tmp >= 10:
            return "pass"
        else:
            if len(all_candles) == 0:
                return "pass"
            candle = self.__select_last_candles(all_candles, "USDT_ETH", 1)[0]
            amount_i_want_to_sell = (current_stockpile.USDT / 2) / candle.close
            return "buy USDT_ETH " + str(amount_i_want_to_sell)

    @staticmethod
    def __select_last_candles(all_candles, pair, number_of_candles):
        last_candles = []
        last_three_candles = all_candles[:-number_of_candles]
        for three_candles in last_three_candles:
            for candle in three_candles:
                if candle.pair == pair:
                    last_candles.append(candle)
        return last_candles
