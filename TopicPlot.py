import time
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

class TopicPlot(object):
    def __init__(self):
        self.words = {}
        self.needRedraw = False 
        
    def watchOn(self, filename):
        filename.seek(0,2)
        while True:
            line = filename.readline()
            if not line:
                # update graph
                if self.needRedraw:
                    wc = WordCloud().generate_from_frequencies(self.words.items())
                    plt.imshow(wc)
                    plt.axis("off")
                    plt.show()
                    self.needRedraw = False
                    print "Word cloud updated."
                time.sleep(0.1)
                continue
            yield line
            self.needRedraw = True

    def start(self):
        filename = "lda_topics.txt"
        file = open(filename,"r")
        updatedLines = self.watchOn(file)
        lastupdate = ""
        print "TopicPlot running. Start watching on file:", filename
        for line in updatedLines:
            # incoming data analysis
            if "time=" in line:
                lastupdate = line.split("=")[1]
                continue
            else:
                for token in line.split(","):
                    token = token.strip()
                    if token == "": continue

                    if self.words.has_key(token):
                        self.words[token] = self.words[token] + 1
                    else:
                        self.words[token] = 1
            if len(self.words) <= 0: continue
            

plot = TopicPlot()
plot.start()
