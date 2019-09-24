from bot.candle import Candle
from bot.indicatorSet import IndicatorSet
from bot.indicatorSet import Trend
import sys

DEBUG_TEXT_MODE = False
DEBUG_PLOT_MODE = False

if DEBUG_PLOT_MODE:
    from bot.drawer import Drawer


class ArtificialIntelligence:
    def __init__(self):
        if DEBUG_PLOT_MODE:
            self.__drawer = Drawer()
        self.__USDT_ETH_indicators = IndicatorSet("USDT_ETH")
        self.__USDT_BTC_indicators = IndicatorSet("USDT_BTC")
        self.__BTC_ETH_indicators = IndicatorSet("BTC_ETH")
        self.__tmp = 1
        self.__lockAction = 0
        self.__sell_permission_USDT_BTC = False
        self.__buy_permission_USDT_BTC = False
        self.__sell_permission_USDT_ETH = False
        self.__buy_permission_USDT_ETH = False
        self.__buy_permission_BTC_ETH = False
        self.__sell_permission_BTC_ETH = False

    def update_stats(self, all_candles):
        self.__USDT_ETH_indicators.feed(all_candles)
        self.__BTC_ETH_indicators.feed(all_candles)
        self.__USDT_BTC_indicators.feed(all_candles)
        if self.__tmp == 319 and DEBUG_PLOT_MODE:
            self.__debug_plot_charts(all_candles)
        self.__tmp += 1

    def decide_action(self, all_candles, current_stockpile, bot_settings):
        self.__lockAction -= 1
        if self.__lockAction > 0:
            return "pass"
        if len(all_candles) < 20:
            return "pass"
        option = 0
        BTC_ETH_action = 0
        USDT_ETH_action = 0
        USDT_BTC_action = 0
        BTC_ETH_action = self.__do_action_on_BTC_ETH(all_candles, current_stockpile, bot_settings, option)
        if BTC_ETH_action:
            option = 1
        USDT_ETH_action = self.__do_action_on_USDT_ETH(all_candles, current_stockpile, bot_settings, option)
        if USDT_ETH_action:
            option = 1
        USDT_BTC_action = self.__do_action_on_USDT_BTC(all_candles, current_stockpile, bot_settings, option)
        if USDT_ETH_action == 0 and USDT_BTC_action == 0 and BTC_ETH_action == 0:
            return "pass"
        else:
            final_action = self.__stick_actions_together(USDT_ETH_action, USDT_BTC_action, BTC_ETH_action)
            if final_action == 0:
                return "pass"
            else:
                self.__lockAction = 6
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
        #if (self.__buy_authorization(self.__USDT_ETH_indicators) and current_stockpile.USDT > 3):
        if (self.__buy_authorization(self.__USDT_ETH_indicators) or self.__buy_permission_USDT_ETH is True) and current_stockpile.USDT > 3:
            if self.__buy_permission_USDT_ETH is False:
                self.__buy_permission_USDT_ETH = True
                return 0
            else:
                self.__buy_permission_USDT_ETH = False
            price_one_eth = Candle.select_last_candles(all_candles, "USDT_ETH", 1)[0].close
            amount_i_want_to_buy = current_stockpile.USDT / price_one_eth
            if option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "buy USDT_ETH " + str(amount_i_want_to_buy)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_ETH_indicators, msg)
            return "buy USDT_ETH " + str(amount_i_want_to_buy)
        #elif self.__sell_authorization(self.__USDT_ETH_indicators):
        elif self.__sell_authorization(self.__USDT_ETH_indicators) or self.__sell_permission_USDT_ETH is True:
            if self.__sell_permission_USDT_ETH is False:
                self.__sell_permission_USDT_ETH = True
                return 0
            else:
                self.__sell_permission_USDT_ETH = False
            amount_i_want_to_sell = current_stockpile.ETH
            if amount_i_want_to_sell < 0.000001 or option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "sell USDT_ETH " + str(amount_i_want_to_sell)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_ETH_indicators, msg)
            return "sell USDT_ETH " + str(amount_i_want_to_sell)
        return 0

    def __do_action_on_BTC_ETH(self, all_candles, current_stockpile, bot_settings, option):
        #if self.__buy_authorization(self.__BTC_ETH_indicators):
        if self.__buy_authorization(self.__BTC_ETH_indicators) or (self.__buy_permission_BTC_ETH is True):
            if self.__buy_permission_BTC_ETH is False:
                self.__buy_permission_BTC_ETH = True
                return 0
            else:
                self.__buy_permission_BTC_ETH = False
            if current_stockpile.BTC > 0:
                price_one_eth = Candle.select_last_candles(all_candles, "BTC_ETH", 1)[0].close
                amount_i_want_to_buy = current_stockpile.BTC / price_one_eth
                if DEBUG_TEXT_MODE:
                    msg = "buy BTC_ETH " + str(amount_i_want_to_buy)
                    self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__BTC_ETH_indicators, msg)
                return "buy BTC_ETH " + str(amount_i_want_to_buy)
        elif self.__sell_authorization(self.__BTC_ETH_indicators) or self.__sell_permission_BTC_ETH is True:
            if self.__sell_permission_BTC_ETH is False:
                self.__sell_permission_BTC_ETH = True
                return 0
            else:
                self.__sell_permission_BTC_ETH = False
            amount_i_want_to_sell = current_stockpile.ETH
            if amount_i_want_to_sell < 0.000001:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "sell BTC_ETH " + str(amount_i_want_to_sell)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__BTC_ETH_indicators, msg)
            return "sell BTC_ETH " + str(amount_i_want_to_sell)
        return 0

    def __do_action_on_USDT_BTC(self, all_candles, current_stockpile, bot_settings, option):
        #if (self.__buy_authorization(self.__USDT_BTC_indicators)) and current_stockpile.USDT > 3:
        if (self.__buy_authorization(self.__USDT_BTC_indicators) or self.__buy_permission_USDT_BTC is True) and current_stockpile.USDT > 3:
            if self.__buy_permission_USDT_BTC is False:
                self.__buy_permission_USDT_BTC = True
                return 0
            else:
                self.__buy_permission_USDT_BTC = False
            price_one_btc = Candle.select_last_candles(all_candles, "USDT_BTC", 1)[0].close
            amount_i_want_to_buy = current_stockpile.USDT / price_one_btc
            if option:
                return 0
            if DEBUG_TEXT_MODE:
                msg = "buy USDT_BTC " + str(amount_i_want_to_buy)
                self.__debug_print_which_indicator_triggered(all_candles, current_stockpile, self.__USDT_BTC_indicators, msg)
            return "buy USDT_BTC " + str(amount_i_want_to_buy)
        #elif self.__sell_authorization(self.__USDT_BTC_indicators):
        elif self.__sell_authorization(self.__USDT_BTC_indicators) or (self.__sell_permission_USDT_BTC is True):
            if self.__sell_permission_USDT_BTC is False:
                self.__sell_permission_USDT_BTC = True
                return 0
            else:
                self.__sell_permission_USDT_BTC = False
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
        """
        if indicators.MACD.buy_indicator and not (indicators.trend.UPWARD and indicators.ADX.ADX[-1] > 23.66) and indicators.BB.BB_indicator:
            return True
        if indicators.ADX.buy_indicator:
            return True
        if indicators.stochastic.buy_indicator:
            return True
        if indicators.RSI.buy_indicator:
            return True
        if indicators.BB.buy_indicator:
            return True
        return False
        """

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
                if indicators.ADX.DI_negative[-1] > 22.90 and indicators.trend == Trend.UPWARD:
                    return False
                if indicators.ADX.trend_strength > 3 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_positive[-1] < 8.8:
                    return False
                if indicators.ADX.trend_strength > 2 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_positive[-1] < 12.71:
                    return False
                if indicators.ADX.trend_strength > 3 and indicators.trend == Trend.DOWNWARD and indicators.ADX.DI_negative[-1] > 35.96 and indicators.ADX.DI_positive[-1] < 14.08:
                    return False
                if indicators.ADX.ADX[-1] > 17.33 and indicators.trend == Trend.DOWNWARD:
                    return False
                if indicators.ADX.DI_negative[-1] > 25.13 and indicators.trend == Trend.DOWNWARD and indicators.stochastic.buy_indicator:
                    return False
                if indicators.trend == Trend.DOWNWARD and indicators.BB.sell_indicator and indicators.ADX.DI_negative[-1] > 28.72:
                    return False
            if indicators.MACD.buy_indicator and indicators.ADX.trend_strength == 0:
                return False
            if indicators.SMA.SMA_160_diff > 48.458 and indicators.trend == Trend.UPWARD and indicators.ADX.trend_strength > 3 and indicators.ADX.DI_positive[-1] < 6.042:
                return False
            if indicators.MACD.buy_indicator and indicators.ADX.ADX[-1] > 23.66:
                return False
            if indicators.BB.buy_indicator and indicators.ADX.ADX[-1] < 7.5:
                return False
            return True
        return False

    @staticmethod
    def __sell_authorization(indicators):
        """
        if indicators.MACD.sell_indicator:
            return True
        if indicators.ADX.sell_indicator:
            return True
        if indicators.stochastic.sell_indicator:
            return True
        if indicators.RSI.sell_indicator:
            return True
        if indicators.BB.sell_indicator:
            return True
        return False
        """


        if (indicators.overbought
                or (indicators.BB.sell_indicator and indicators.BB.BB_indicator and not indicators.possible_oversold and not indicators.ADX.buy_indicator)
                or (indicators.MACD.sell_indicator and indicators.BB.BB_indicator and not indicators.possible_oversold)
                or (indicators.ADX.sell_indicator and indicators.ADX.trend_strength < 2)):
            if indicators.stochastic.sell_indicator or indicators.RSI.sell_indicator:
                if (indicators.ADX.trend_strength > 5 and indicators.trend == Trend.UPWARD) or indicators.ADX.trend_strength == 0:
                    return False
                if indicators.MACD.buy_indicator and indicators.BB.buy_indicator:
                    return False
                if indicators.trend == Trend.UPWARD and indicators.ADX.DI_positive[-1] > 33.0 and indicators.ADX.DI_negative[-1] > 15.29:
                    return False
                if indicators.ADX.DI_negative[-1] < 6.52 and indicators.ADX.trend_strength > 2 and indicators.trend == Trend.UPWARD:
                    return False
                if indicators.ADX.buy_indicator and not indicators.BB.BB_indicator:
                    return False
                if indicators.SMA.SMA_160_diff > 46.7 and indicators.trend == Trend.UPWARD and indicators.ADX.ADX[-1] > 29.22 and indicators.ADX.DI_positive[-1] > 25.03 and indicators.ADX.DI_negative[-1] < 13:
                    return False
                #if indicators.ADX.ADX[-1] > 28.59 and indicators.trend == Trend.UPWARD and not indicators.RSI.sell_indicator:
                    #return False
                if indicators.RSI.sell_indicator and indicators.RSI.RSI[-1] > 70:
                    return False
                if indicators.ADX.ADX[-1] > 36.29 and indicators.trend == Trend.UPWARD:
                    return False
            if indicators.MACD.sell_indicator:
                if indicators.stochastic.stochastic_D[-1] < 44.1:
                    return False
                if indicators.ADX.trend_strength == 0:
                    return False
            """
            if indicators.SMA.SMA_160_diff > 22.24 and indicators.trend == Trend.UPWARD and indicators.ADX.trend_strength < 2:
                return False
            #if indicators.SMA.SMA_160_diff > 46.7 and indicators.trend == Trend.UPWARD and indicators.ADX.trend_strength >= 3:
                #return False
            if indicators.SMA.SMA_160_diff > 72.94 and indicators.trend == Trend.UPWARD:
                return False
            """
            return True
        if indicators.ADX.ADX[-1] > 31.46 and indicators.trend == Trend.DOWNWARD and indicators.SMA.SMA_160_diff > 28.98:
            return True
        return False

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
        if indicators.overbought:
            print("Overbought triggered", file=sys.stderr)
        if indicators.oversold:
            print("Oversold triggered", file=sys.stderr)
        if indicators.possible_overbought:
            print("possible Overbought triggered", file=sys.stderr)
        if indicators.possible_oversold:
            print("possible Oversold triggered", file=sys.stderr)
        print("MSG = ", msg, file=sys.stderr)
        print("sto_D  = ", indicators.stochastic.stochastic_D[-20:], file=sys.stderr)
        print("RSI  = ", indicators.RSI.RSI[-20:], file=sys.stderr)
        print("ADX strength : ", indicators.ADX.ADX[-1], file=sys.stderr)
        print("DI+ strength : ", indicators.ADX.DI_positive[-1], file=sys.stderr)
        print("DI- strength : ", indicators.ADX.DI_negative[-1], file=sys.stderr)
        print("current USDT =", stockpile.USDT, " current ETH = ", stockpile.ETH, "current BTC = ", stockpile.BTC, file=sys.stderr)

        last_close = Candle.select_last_candles(all_candles, "BTC_ETH", 1)[-1].close
        print("diff SMA_160 - close : ", indicators.SMA.SMA_160_diff, file=sys.stderr)
        print("diff EMA_80 - close : ", last_close - indicators.EMA.EMA_80[-1], file=sys.stderr)
        print("diff SMA_50 - close : ", last_close - indicators.SMA.SMA_50[-1], file=sys.stderr)
        print("", file=sys.stderr)
