import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class CatPlot(object):
    def __init__(self):
        self.filename = "categories.txt"
        print "CatPlot running. Start watching on file:", self.filename
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        self.data = {}

    def animate(self, i):
        file = open(self.filename)
        self.data = {}
        for line in file:
            line = line.strip()
            if line == "": continue
            if "time=" in line:
                continue
            else:
                for token in line.split(";"):
                    keyValue = token.split("=")
                    if self.data.has_key(keyValue[0]):
                        self.data[keyValue[0]] = int(self.data[keyValue[0]]) + int(keyValue[1])
                    else:
                        self.data[keyValue[0]] = int(keyValue[1])
        if len(self.data) > 0:
            self.ax1.clear()
            x_pos = np.arange(len(self.data))
            self.ax1.bar(x_pos, self.data.values())
            width = 0.8
            plt.xticks(x_pos + width / 2, self.data.keys())

    def start(self):
        ani = animation.FuncAnimation(self.fig, self.animate, interval=100)
        plt.show()

plot = CatPlot()
plot.start()
