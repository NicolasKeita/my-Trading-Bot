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
