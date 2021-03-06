from bot.inputParser import InputParser, ExitProgram
from bot.stockpile import Stockpile
from bot.botSettings import BotSettings
from bot.artificialIntelligence import ArtificialIntelligence


class Bot:
    def __init__(self):
        self.input_parser = InputParser()
        self.stockpile = Stockpile()
        self.bot_settings = BotSettings()
        self.all_candles = []
        self.ai = ArtificialIntelligence()

    def run(self):
        while True:
            try:
                stdin_input = self.input_parser.get_input()

            except (EOFError, ExitProgram, KeyboardInterrupt):
                return
            self.__handle_input(stdin_input)

    def __handle_input(self, stdin_input):
        if stdin_input[0] == "settings":
            self.__set_bot_settings(stdin_input[1], stdin_input[2])
        elif stdin_input[0] == "update":
            if stdin_input[1] == "game":
                if stdin_input[2] == "next_candles":
                    self.__update_candle_list(stdin_input[3])
                elif stdin_input[2] == "stacks":
                    self.__update_stockpile(stdin_input[3])
        elif stdin_input[0] == "action":
            action = self.ai.decide_action(self.all_candles, self.stockpile,
                                           self.bot_settings)
            print(action)

    def __set_bot_settings(self, setting_type, value):
        if setting_type == "initial_stack":
            self.stockpile.USDT = float(value)
        elif setting_type == "transaction_fee_percent":
            self.bot_settings.transaction_fee_percent = float(value)

    def __update_candle_list(self, input_candles):
        three_candles = self.input_parser.parse_three_candles(input_candles)
        self.all_candles.append(three_candles)
        self.ai.update_stats(self.all_candles)

    def __update_stockpile(self, input_new_stockpile):
        new_stockpile_formatted = \
            self.input_parser.parse_new_stockpile(input_new_stockpile)
        self.stockpile.USDT = new_stockpile_formatted[0]
        self.stockpile.BTC = new_stockpile_formatted[1]
        self.stockpile.ETH = new_stockpile_formatted[2]

    def get_selected_candles(self, currency):
        selected_candles = []
        for three_candles in self.all_candles:
            selected_candles.append(three_candles[currency])
        return selected_candles
