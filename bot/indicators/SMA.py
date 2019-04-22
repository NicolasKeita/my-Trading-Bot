class SMA:
    def __init__(self):
        self.SMA_12 = []
        self.SMA_20 = []
        self.SMA_26 = []
        self.SMA_80 = []
        self.SMA_85 = []
        self.SMA_90 = []
        self.SMA_160 = []

    @staticmethod
    def SMA(data_list):
        if len(data_list) == 0:
            return 0
        moving_average = 0
        for number in data_list:
            moving_average += number
        moving_average /= len(data_list)
        return moving_average
