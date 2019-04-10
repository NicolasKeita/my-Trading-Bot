from enum import IntEnum, unique

@unique
class CurrencyEnum(IntEnum):
    USDT_ETH = 0
    USDT_BTC = 1
    BTC_ETH = 2
