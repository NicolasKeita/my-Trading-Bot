class SMA:
    def __init__(self):
        self.SMA_12 = []
        self.SMA_20 = []
        self.SMA_26 = []
        self.SMA_50 = []
        self.SMA_80 = []
        self.SMA_85 = []
        self.SMA_90 = []
        self.SMA_95 = []
        self.SMA_100 = []
        self.SMA_160 = []
        self.SMA_160_diff = 0

    @staticmethod
    def SMA(data_list):
        if len(data_list) == 0:
            return 0
        moving_average = 0
        for number in data_list:
            moving_average += number
        moving_average /= len(data_list)
        return moving_average

    def update_SMA_160_diff(self, last_closing_price):
        self.SMA_160_diff = ((abs(self.SMA_160[-1] - last_closing_price)) /
                             ((self.SMA_160[-1] + last_closing_price) / 2)) * 1000
