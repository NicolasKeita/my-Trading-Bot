import matplotlib.pyplot as plt
import matplotlib.dates as dates
import sys

class Drawer:
    def __init__(self):
        pass

    def draw(self, y, x, EMA_12, EMA_26, MACD, MACD_signal):
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
        plt.legend()
        plt.show()
        print("PLOT", file=sys.stderr)
        print(y[0])
