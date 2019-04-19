class IndicatorSet:
    def __init__(self):
        self.SMA_12 = []
        self.SMA_20 = []
        self.SMA_26 = []
        self.SMA_80 = []
        self.SMA_160 = []
        self.EMA_12 = []
        self.EMA_20 = []
        self.EMA_26 = []
        self.EMA_80 = []
        self.EMA_160 = []
        self.MACD = []
        self.MACD_signal = []
        self.MACD_buy_indicator = False
        self.MACD_sell_indicator = False
        self.standard_deviation = []
        self.BBW = []
        self.BB_indicator = False
