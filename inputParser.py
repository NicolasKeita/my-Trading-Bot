from sys import stderr

from candle import Candle


class InputParser:
    def __init__(self, settings, candles_list):
        self.settings = settings
        self.candles_list = candles_list

    def do_infinite_input_parsing(self):
        i = 0
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line.endswith('\n'):
                line = line[:-1]
            parts = line.split(" ")
            if parts[0] == "settings":
                self.set_setting(parts[1], parts[2:])
            elif parts[0] == "update":
                self.handle_update_type_input(parts[1], parts[2], parts[3])
            elif parts[0] == "action":
                i += 1
                if i >= 10:
                    print("pass")
                else:
                    candle = self.select_last_candle("USDT_ETH")
                    amount_i_want_to_sell = (self.settings.USDT_stockpile / 2) / candle.close
                    print("buy USDT_ETH", amount_i_want_to_sell)

    def select_last_candle(self, pair):
        candles = self.candles_list[-1]
        for candle in candles:
            if candle.pair == pair:
                return candle

    def handle_update_type_input(self, player, update_type, value):
        if player == "game":
            if update_type == "next_candles":
                self.parse_candles_value(value)
            elif update_type == "stacks":
                self.parse_new_stacks(value)

    def parse_new_stacks(self, value):
        stacks = value.split(',')
        for stack in stacks:
            parts = stack.split(':')
            if parts[0] == "BTC":
                self.settings.BTC_stockpile = float(parts[1])
            elif parts[0] == "ETH":
                self.settings.ETH_stockpile = float(parts[1])
            elif parts[0] == "USDT":
                self.settings.USDT_stockpile = float(parts[1])

    def parse_candles_value(self, value):
        three_candles = [Candle("USDT_ETH"), Candle("USDT_BTC"), Candle("BTC_ETH")]
        candles_input = value.split(';')
        for candle_input in candles_input:
            candle_part = candle_input.split(',')
            for candle in three_candles:
                if candle.pair == candle_part[0]:
                    candle.date = float(candle_part[1])
                    candle.high = float(candle_part[2])
                    candle.low = float(candle_part[3])
                    candle.open = float(candle_part[4])
                    candle.close = float(candle_part[5])
                    candle.volume = float(candle_part[6])
        self.candles_list.append(three_candles)
        if len(self.candles_list) > 20:
            self.candles_list.pop(0)

    def set_setting(self, setting_type, value):
        if setting_type == "initial_stack":
            self.settings.USDT_stockpile = float(value[0])
        elif setting_type == "transaction_fee_percent":
            self.settings.transaction_fee_percent = float(value[0])

    @staticmethod
    def percent(nbr, percent):
        return nbr - nbr * percent / 100
