#!/usr/bin/python3

from inputParser import InputParser
from settings import Settings
from candle import Candle


def main():
    settings = Settings()
    candles_list = []
    #candles_list = [[Candle("USDT_ETH"), Candle("USDT_BTC"), Candle("BTC_ETH")]]
    p = InputParser(settings, candles_list)

    p.do_infinite_input_parsing()


if __name__ == "__main__":
    main()
