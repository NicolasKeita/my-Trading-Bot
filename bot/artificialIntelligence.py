from bot.dataSet import DataSet, Trend
from bot.drawer import Drawer
from bot.candle import Candle
import sys

DEBUG_TEXT_MODE = True
DEBUG_PLOT_MODE = False


class ArtificialIntelligence:
    def __init__(self):
        self.__drawer = Drawer()
        self.__data = DataSet()
        self.__tmp = 1

    def update_stats(self, all_candles):
        self.__data.feed(all_candles)
        if self.__tmp == 310 and DEBUG_PLOT_MODE:
            self.__debug_plot_charts(all_candles)
        self.__tmp += 1

    def decide_action(self, all_candles, current_stockpile, bot_settings):
        if len(all_candles) == 0:
            return "pass"
        if self.__data.USDT_ETH.trend == Trend.UPWARD \
                and current_stockpile.USDT > 0 \
                and (self.__data.USDT_ETH.MACD_buy_indicator
                     or self.__data.USDT_ETH.stochastic_buy_indicator):
            price_one_eth = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[0].close
            amount_i_want_to_buy = self.__percent(current_stockpile.USDT / price_one_eth,
                                                  bot_settings.transaction_fee_percent)
            if DEBUG_TEXT_MODE:
                self.__debug_print_which_indicator_triggered()
            return "buy USDT_ETH " + str(amount_i_want_to_buy)
        elif self.__data.USDT_ETH.trend == Trend.DOWNWARD \
                and current_stockpile.ETH > 0 \
                and (self.__data.USDT_ETH.MACD_sell_indicator
                     or self.__data.USDT_ETH.stochastic_sell_indicator):
            amount_i_want_to_sell = current_stockpile.ETH
            if DEBUG_TEXT_MODE:
                self.__debug_print_which_indicator_triggered()
            return "sell USDT_ETH " + str(amount_i_want_to_sell)
        return "pass"

    @staticmethod
    def __percent(nbr, percentage):
        return nbr * (1 - percentage / 100)

    def __debug_plot_charts(self, all_candles):
        all_USDT_ETH_candles = Candle.select_last_candles(all_candles, "USDT_ETH", -1)
        closing_prices = Candle.select_closing_prices(all_USDT_ETH_candles)
        dates = Candle.select_dates(all_USDT_ETH_candles)
        self.__drawer.draw(closing_prices, dates,
                           self.__data.USDT_ETH.EMA_12, self.__data.USDT_ETH.EMA_26,
                           self.__data.USDT_ETH.MACD, self.__data.USDT_ETH.MACD_signal,
                           self.__data.USDT_ETH.stochastic_D)

    def __debug_print_which_indicator_triggered(self):
        if self.__data.USDT_ETH.BB_indicator:
            print("BB indicator triggered", file=sys.stderr)
        if self.__data.USDT_ETH.stochastic_buy_indicator:
            print("stochastic buy indicator triggered", file=sys.stderr)
        if self.__data.USDT_ETH.stochastic_sell_indicator:
            print("stochastic sell indicator triggered", file=sys.stderr)
        if self.__data.USDT_ETH.MACD_buy_indicator:
            print("MACD buy indicator triggered", file=sys.stderr)
        if self.__data.USDT_ETH.MACD_sell_indicator:
            print("MACD sell indicator triggered", file=sys.stderr)
        if self.__data.USDT_ETH.trend == Trend.UPWARD:
            print("TREND UPWARD ", file=sys.stderr)
        if self.__data.USDT_ETH.trend == Trend.DOWNWARD:
            print("TREND DOWNWARD ", file=sys.stderr)
        print("", file=sys.stderr)

