#!/usr/bin/python3

from bot.inputParser import InputParser
from bot.settings import Settings


def main():
    settings = Settings()
    candles_list = []
    p = InputParser(settings, candles_list)

    p.do_infinite_input_parsing()


if __name__ == "__main__":
    main()
