from bot.dataSet import DataSet
from bot.drawer import Drawer
from bot.candle import Candle

DEBUG_PLOT_CHART_MODE = False


class ArtificialIntelligence:
    def __init__(self):
        self.__drawer = Drawer()
        self.__data = DataSet()
        self.__tmp = 1

    def update_stats(self, all_candles):
        self.__data.feed(all_candles)
        # draw chart
        if self.__tmp == 310 and DEBUG_PLOT_CHART_MODE:
            all_USDT_ETH_candles = Candle.select_last_candles(all_candles, "USDT_ETH", -1)
            closing_prices = Candle.select_closing_prices(all_USDT_ETH_candles)
            dates = Candle.select_dates(all_USDT_ETH_candles)
            self.__drawer.draw(closing_prices, dates,
                               self.__data.USDT_ETH.EMA_12, self.__data.USDT_ETH.EMA_26,
                               self.__data.USDT_ETH.MACD, self.__data.USDT_ETH.MACD_signal)
        self.__tmp += 1

    def decide_action(self, all_candles, current_stockpile, bot_settings):
        if len(all_candles) == 0:
            return "pass"
        if self.__data.USDT_ETH.MACD_buy_indicator and self.__data.USDT_ETH.BB_indicator:
            price_one_eth = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[0].close
            amount_i_want_to_buy = self.__percent(current_stockpile.USDT / price_one_eth,
                                                  bot_settings.transaction_fee_percent)
            return "buy USDT_ETH " + str(amount_i_want_to_buy)
        elif self.__data.USDT_ETH.MACD_sell_indicator and self.__data.USDT_ETH.BB_indicator and current_stockpile.ETH > 0:
            amount_i_want_to_sell = current_stockpile.ETH
            return "sell USDT_ETH " + str(amount_i_want_to_sell)
        return "pass"

    @staticmethod
    def __percent(nbr, percentage):
        return nbr * (1 - percentage / 100)

