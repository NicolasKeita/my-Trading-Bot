from sys import stderr


class InputParser:
    def __init__(self, settings, candles):
        self.settings = settings
        self.candles = candles

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
                    print(candle.close, file=stderr)
                    action_USDT_ETH = candle.close
                    amount_i_want_to_sell = (self.settings.USDT_stockpile / 2) / action_USDT_ETH
                    print("buy USDT_ETH", amount_i_want_to_sell)
                    self.settings.ETH_stockpile += InputParser.percent(amount_i_want_to_sell, self.settings.transaction_fee_percent)
                    self.settings.USDT_stockpile -= self.settings.USDT_stockpile / 2

    def select_last_candle(self, pair):
        for candle in self.candles:
            if candle.pair == pair:
                return candle

    def handle_update_type_input(self, player, update_type, value):
        if player == "game":
            if update_type == "next_candles":
                self.parse_candles_value(value)

    def parse_candles_value(self, value):
        candles_input = value.split(';')
        for candle_input in candles_input:
            candle_part = candle_input.split(',')
            for candle in self.candles:
                if candle.pair == candle_part[0]:
                    candle.date = float(candle_part[1])
                    candle.high = float(candle_part[2])
                    candle.low = float(candle_part[3])
                    candle.open = float(candle_part[4])
                    candle.close = float(candle_part[5])
                    candle.volume = float(candle_part[6])

    def set_setting(self, setting_type, value):
        if setting_type == "initial_stack":
            self.settings.USDT_stockpile = float(value[0])
        elif setting_type == "transaction_fee_percent":
            self.settings.transaction_fee_percent = float(value[0])

    @staticmethod
    def percent(nbr, percent):
        return nbr - nbr * percent / 100
