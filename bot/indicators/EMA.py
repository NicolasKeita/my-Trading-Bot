class EMA:
    def __init__(self):
        self.EMA_12 = []
        self.EMA_20 = []
        self.EMA_26 = []
        self.EMA_50 = []
        self.EMA_80 = []
        self.EMA_85 = []
        self.EMA_90 = []
        self.EMA_160 = []

    @staticmethod
    def EMA(data_list, previous_EMA):
        period = len(data_list)
        weigth = 2 / (period + 1)
        current_EMA = data_list[-1] * weigth + previous_EMA * (1 - weigth)
        return current_EMA
