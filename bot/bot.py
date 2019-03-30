from inputParser import InputParser
from stockpile import Stockpile
from botSettings import BotSettings
from artificialIntelligence import  ArtificialIntelligence


class Bot:
    def __init__(self):
        self.inputParser = InputParser()
        self.stockpile = Stockpile()
        self.botSettings = BotSettings()
        self.list_of_three_candles = []
        self.ai = ArtificialIntelligence()

    def run(self):
        while True:
            try:
                stdin_input = self.inputParser.parse_next_input()
            except EOFError:
                return
            self.handle_input(stdin_input)

    def handle_input(self, stdin_input):
        if stdin_input[0] == "settings":
            self.set_bot_settings(stdin_input[1], stdin_input[2])
        elif stdin_input[0] == "update":
            if stdin_input[1] == "game":
                if stdin_input[2] == "next_candles":
                    self.update_candle_list(stdin_input[3])
                elif stdin_input[2] == "stacks":
                    self.update_stockpile(stdin_input[3])
        elif stdin_input[0] == "action":
            action = self.ai.decide_action(self.list_of_three_candles,
                                           self.stockpile)
            print(action)

    def set_bot_settings(self, setting_type, value):
        if setting_type == "initial_stack":
            self.stockpile.USDT = float(value[0])
        elif setting_type == "transaction_fee_percent":
            self.botSettings.transaction_fee_percent = float(value[0])

    def update_candle_list(self, input_candles):
        three_candles = self.inputParser.parse_three_candles(input_candles)
        self.list_of_three_candles.append(three_candles)
        if len(self.list_of_three_candles) > 20:
            self.list_of_three_candles.pop(0)

    def update_stockpile(self, input_new_stockpile):
        new_stockpile_formatted = \
            self.inputParser.parse_new_stockpile(input_new_stockpile)
        self.stockpile.USDT = new_stockpile_formatted[0]
        self.stockpile.BTC = new_stockpile_formatted[1]
        self.stockpile.ETH = new_stockpile_formatted[2]

