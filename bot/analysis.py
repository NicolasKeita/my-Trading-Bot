class Analysis:
    @staticmethod
    def SMA(data_list):
        if len(data_list) == 0:
            return 0
        moving_average = 0
        for number in data_list:
            moving_average += number
        moving_average /= len(data_list)
        return moving_average

    @staticmethod
    def EMA(data_list, previous_EMA):
        period = len(data_list)
        weigth = 2 / (period + 1)
        current_EMA = data_list[-1] * weigth + previous_EMA * (1 - weigth)
        return current_EMA
