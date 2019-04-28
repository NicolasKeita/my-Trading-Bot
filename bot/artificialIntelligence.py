from bot.drawer import Drawer
from bot.candle import Candle
from bot.indicatorSet import IndicatorSet
from bot.indicatorSet import Trend
from time import time
import sys

DEBUG_TEXT_MODE = True
DEBUG_PLOT_MODE = False


class ArtificialIntelligence:
    def __init__(self):
        self.__drawer = Drawer()
        self.__USDT_ETH_indicators = IndicatorSet("USDT_ETH")
        self.__USDT_BTC_indicators = IndicatorSet("USDT_BTC")
        self.__BTC_ETH_indicators = IndicatorSet("BTC_ETH")
        self.__tmp = 1

    def update_stats(self, all_candles):
        self.__USDT_ETH_indicators.feed(all_candles)
        self.__BTC_ETH_indicators.feed(all_candles)
        self.__USDT_BTC_indicators.feed(all_candles)
        if self.__tmp == 319 and DEBUG_PLOT_MODE:
            self.__debug_plot_charts(all_candles)
        self.__tmp += 1

    def decide_action(self, all_candles, current_stockpile, bot_settings):
        if len(all_candles) < 20:
            return "pass"
        option = 0
        BTC_ETH_action = 0
        USDT_ETH_action = 0
        USDT_BTC_action = 0
        #BTC_ETH_action = self.__do_action_on_BTC_ETH(all_candles, current_stockpile, bot_settings, option)
        if BTC_ETH_action:
            option = 1
        USDT_ETH_action = self.__do_action_on_USDT_ETH(all_candles, current_stockpile, bot_settings, option)
        if USDT_ETH_action:
            option = 1
        #USDT_BTC_action = self.__do_action_on_USDT_BTC(all_candles, current_stockpile, bot_settings, option)
        if USDT_ETH_action == 0 and USDT_BTC_action == 0 and BTC_ETH_action == 0:
            return "pass"
        else:
            final_action = self.__stick_actions_together(USDT_ETH_action, USDT_BTC_action, BTC_ETH_action)
            if final_action == 0:
                return "pass"
            else:
                return final_action

    def __stick_actions_together(self, str1, str2, str3):
        two_actions = self.__stick_two_actions_together(str1, str2)
        return self.__stick_two_actions_together(two_actions, str3)

    @staticmethod
    def __stick_two_actions_together(str1, str2):
        if str1 and str2:
            return str1 + ";" + str2
        elif not str1 and not str2:
            return 0
        elif not str1 and str2:
            return str2
        elif str1 and not str2:
            return str1
        else:
            return 0

    def __do_action_on_USDT_ETH(self, all_candles, current_stockpile, bot_settings, option):
        if self.__buy_authorization(self.__USDT_ETH_indicators) and current_stockpile.USDT > 3:
            price_one_eth = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[0].close
            amount_i_want_to_buy = self.__percent((current_stockpile.USDT / 1) / price_one_eth,
                                                  bot_settings.transaction_fee_percent)
            if option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "buy USDT_ETH " + str(amount_i_want_to_buy)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_ETH_indicators, msg)
            return "buy USDT_ETH " + str(amount_i_want_to_buy)
        elif self.__sell_authorization(self.__USDT_ETH_indicators):
            amount_i_want_to_sell = current_stockpile.ETH
            if amount_i_want_to_sell < 0.000001 or option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "sell USDT_ETH " + str(amount_i_want_to_sell)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_ETH_indicators, msg)
            return "sell USDT_ETH " + str(amount_i_want_to_sell)
        return 0

    def __do_action_on_BTC_ETH(self, all_candles, current_stockpile, bot_settings, option):
        if self.__buy_authorization(self.__BTC_ETH_indicators):
            if current_stockpile.BTC > 0:
                price_one_eth = Candle.select_last_candles(all_candles, "BTC_ETH", 1)[0].close
                amount_i_want_to_buy = self.__percent((current_stockpile.BTC / 1) / price_one_eth,
                                                      bot_settings.transaction_fee_percent)
                if DEBUG_TEXT_MODE:
                    msg = "buy BTC_ETH " + str(amount_i_want_to_buy)
                    self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__BTC_ETH_indicators, msg)
                return "buy BTC_ETH " + str(amount_i_want_to_buy)
        elif self.__sell_authorization(self.__BTC_ETH_indicators):
            amount_i_want_to_sell = current_stockpile.ETH
            if amount_i_want_to_sell < 0.000001:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "sell BTC_ETH " + str(amount_i_want_to_sell)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__BTC_ETH_indicators, msg)
            return "sell BTC_ETH " + str(amount_i_want_to_sell)
        return 0

    def __do_action_on_USDT_BTC(self, all_candles, current_stockpile, bot_settings, option):
        if self.__buy_authorization(self.__USDT_BTC_indicators) and current_stockpile.USDT > 3:
            price_one_btc = Candle.select_last_candles(all_candles, "USDT_BTC", 1)[0].close
            amount_i_want_to_buy = self.__percent((current_stockpile.USDT / 1) / price_one_btc,
                                                  bot_settings.transaction_fee_percent)
            if option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "buy USDT_BTC " + str(amount_i_want_to_buy)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_BTC_indicators, msg)
            return "buy USDT_BTC " + str(amount_i_want_to_buy)
        elif self.__sell_authorization(self.__USDT_BTC_indicators):
            amount_i_want_to_sell = current_stockpile.BTC
            if amount_i_want_to_sell < 0.000001 or option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "sell USDT_BTC " + str(amount_i_want_to_sell)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_BTC_indicators, msg)
            return "sell USDT_BTC " + str(amount_i_want_to_sell)
        return 0

    @staticmethod
    def __buy_authorization(indicators):
        #if indicators.ADX.buy_authorized is True:
        if (indicators.oversold
                or (indicators.BB.buy_indicator and indicators.BB.BB_indicator and not indicators.possible_overbought)
                or (indicators.MACD.buy_indicator and indicators.BB.BB_indicator and not indicators.possible_overbought)
                or (indicators.MACD.buy_indicator and indicators.BB.buy_indicator and indicators.BB.BB_indicator)
                or indicators.ADX.buy_indicator and indicators.ADX.trend_strength < 2):
            if indicators.stochastic.buy_indicator or indicators.RSI.buy_indicator:
                if indicators.ADX.trend_strength > 5 and indicators.trend == Trend.DOWNWARD:
                    return False
                if indicators.ADX.trend_strength > 3 and indicators.trend == Trend.UPWARD and indicators.ADX.DI_negative[-1] > 26.1220:
                    return False
                if indicators.ADX.DI_negative[-1] > 29.649 and indicators.trend == Trend.UPWARD:
                    return False
                if indicators.ADX.trend_strength > 3 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_positive[-1] < 8.8:
                    return False
                if indicators.ADX.trend_strength > 2 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_positive[-1] < 12.71:
                    return False
                if indicators.ADX.trend_strength > 3 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_negative[-1] > 35.96 and indicators.ADX.DI_positive[-1] < 14.08:
                    return False
            if (indicators.MACD.buy_indicator and indicators.ADX.trend_strength == 0):
                return False
            return True
        return False

    @staticmethod
    def __sell_authorization(indicators):
        #if indicators.ADX.sell_authorized is True:
        if (indicators.overbought
                or (indicators.BB.sell_indicator and indicators.BB.BB_indicator and not indicators.possible_oversold)
                or (indicators.MACD.sell_indicator and indicators.BB.BB_indicator and not indicators.possible_oversold)
                or (indicators.ADX.sell_indicator and indicators.ADX.trend_strength < 2)):
            if indicators.stochastic.sell_indicator or indicators.RSI.sell_indicator:
                if (indicators.ADX.trend_strength > 5 and indicators.trend == Trend.UPWARD) or indicators.ADX.trend_strength == 0:
                    return False
                if (indicators.MACD.buy_indicator and indicators.BB.buy_indicator):
                    return False
                if indicators.ADX.DI_positive[-1] > 31.148:
                    return False
            if indicators.MACD.sell_indicator:
                if indicators.ADX.trend_strength == 0:
                    return False
            return True
        return False

    @staticmethod
    def __percent(nbr, percentage):
        return nbr * (1 - percentage / 100)

    def __debug_plot_charts(self, all_candles):
        all_USDT_ETH_candles = Candle.select_last_candles(all_candles, "USDT_ETH", -1)
        closing_prices = Candle.select_closing_prices(all_USDT_ETH_candles)
        dates = Candle.select_dates(all_USDT_ETH_candles)
        self.__drawer.draw(closing_prices, dates,
                           self.__USDT_ETH_indicators.EMA.EMA_12, self.__USDT_ETH_indicators.EMA.EMA_26,
                           self.__USDT_ETH_indicators.MACD.MACD, self.__USDT_ETH_indicators.MACD.MACD_signal,
                           self.__USDT_ETH_indicators.stochastic.stochastic_D, self.__USDT_ETH_indicators.RSI.RSI,
                           self.__USDT_ETH_indicators.ADX.ADX)

    def __debug_print_which_indicator_triggered(self, all_candles, stockpile, indicators, msg):
        if indicators.BB.buy_indicator:
            print("BB_buy indicator triggered", file=sys.stderr)
        if indicators.BB.sell_indicator:
            print("BB_ sell _indicator_ triggered", file=sys.stderr)
        if indicators.BB.BB_indicator:
            print("BB indicator triggered", file=sys.stderr)
        if indicators.stochastic.buy_indicator:
            print("stochastic buy indicator triggered", file=sys.stderr)
        if indicators.stochastic.sell_indicator:
            print("stochastic sell indicator triggered", file=sys.stderr)
        if indicators.MACD.buy_indicator:
            print("MACD buy indicator triggered", file=sys.stderr)
        if indicators.MACD.sell_indicator:
            print("MACD sell indicator triggered", file=sys.stderr)
        if indicators.trend == Trend.UPWARD:
            print("TREND UPWARD ", file=sys.stderr)
        if indicators.trend == Trend.DOWNWARD:
            print("TREND DOWNWARD ", file=sys.stderr)
        if indicators.RSI.buy_indicator:
            print("RSI buy indicator triggered", file=sys.stderr)
        if indicators.RSI.sell_indicator:
            print("RSI sell indicator triggered", file=sys.stderr)
        if indicators.ADX.buy_indicator:
            print("ADX buy indicator triggered", file=sys.stderr)
        if indicators.ADX.sell_indicator:
            print("ADX sell indicator triggered", file=sys.stderr)
        print("MSG = ", msg, file=sys.stderr)
        print("sto_D  = ", indicators.stochastic.stochastic_D[-20:], file=sys.stderr)
        print("RIS  = ", indicators.RSI.RSI[-20:], file=sys.stderr)
        print("ADX strength : ", indicators.ADX.ADX[-1], file=sys.stderr)
        print("DI+ strength : ", indicators.ADX.DI_positive[-1], file=sys.stderr)
        print("DI- strength : ", indicators.ADX.DI_negative[-1], file=sys.stderr)
        '''
        last_close = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[-1].close
        print("diff EMA_80 - close : ", last_close - indicators.EMA.EMA_80[-1], file=sys.stderr)
        print("diff EMA_50 - close : ", last_close - indicators.SMA.SMA_50[-1], file=sys.stderr)
        print("Current USDT = ", stockpile.USDT, file=sys.stderr)
        '''
        print("", file=sys.stderr)
