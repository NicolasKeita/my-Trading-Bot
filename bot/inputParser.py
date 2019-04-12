from bot.candle import Candle


class InputParser:
    @staticmethod
    def get_input():
        line = input()
        if line.endswith('\n'):
            line = line[:-1]
        if line == "exit":
            raise ExitProgram
        return line.split(" ")

    # return a list : the new amount of USDT, BTC, ETH. In that order.
    @staticmethod
    def parse_new_stockpile(new_stockpile):
        separated_stockpile = new_stockpile.split(',')
        new_stockpile_formmated = []
        for currency_stack in separated_stockpile:
            parts = currency_stack.split(':')
            if parts[0] == "USDT":
                USDT_new_stack = float(parts[1])
            elif parts[0] == "BTC":
                BTC_new_stack = float(parts[1])
            elif parts[0] == "ETH":
                ETH_new_stack = float(parts[1])
        new_stockpile_formmated.append(USDT_new_stack)
        new_stockpile_formmated.append(BTC_new_stack)
        new_stockpile_formmated.append(ETH_new_stack)
        return new_stockpile_formmated

    @staticmethod
    def parse_three_candles(value):
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
        return three_candles

    @staticmethod
    def percent(nbr, percent):
        return nbr - nbr * percent / 100


class ExitProgram(Exception):
    pass
