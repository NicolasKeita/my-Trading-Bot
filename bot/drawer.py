import matplotlib.pyplot as plt
import matplotlib.dates as dates
import numpy as np
import sys

class Drawer:
    def __init__(self):
        pass

    def draw(self, y, x, EMA_12, EMA_26, MACD, MACD_signal, stochastic_D):
        plt.title("USDT_ETH_charts")
        plt.xlabel("time")
        plt.ylabel("close_price")
        date = []
        for time in x:
            date.append(dates.epoch2num(time))
        plt.plot_date(date, y, '-', label="USDT_ETH")
        plt.plot_date(date[11:], EMA_12, '-', label="EMA_12")
        plt.plot_date(date[25:], EMA_26, '-', label="EMA_26")
        plt.plot_date(date[25:], MACD, '-', label="MACD")
        plt.plot_date(date[25 + 9:], MACD_signal, '-', label="MACD_signal")
        print(len(stochastic_D))
        plt.plot_date(date[14 * 24 * 2 + 5:], [x + 600 for x in stochastic_D], '-', label="stochastic_D")
        plt.plot_date(date, np.full((1, len(date)), 80 + 600)[0], '-', label="80")
        plt.plot_date(date, np.full((1, len(date)), 20 + 600)[0], '-', label="20")
        plt.legend()
        plt.show()
        print("PLOT", file=sys.stderr)
        print(y[0])
