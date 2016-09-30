# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import time

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
	pullData = open('categories.txt','r').read()
	dataArray = pullData.split('\n')
	tar = [0,0,0,0,0,0]
	xar = []
	y1ar = []
	y2ar = []
	y3ar = []
	y4ar = []
	for eachLine in dataArray:
		if eachLine.strip() != '':
			if eachLine.find('time') >= 0:
				a,x = eachLine.split('=', 1)
				if tar[0]!= x:
					xar.append(tar[0])
					tar[0]=x
					tar[5]=0
				else:
					tar[5]=1
			if eachLine.find('news') >= 0:
				n,c,m,o = eachLine.split(';', 3)
				n1,y1 = n.split('=', 1)
				c1,y2 = c.split('=', 1)
				m1,y3 = m.split('=', 1)
				o1,y4 = o.split('=', 1)
				if tar[5] == 0:
					y1ar.append(tar[1])
					y2ar.append(tar[2])
					y3ar.append(tar[3])
					y4ar.append(tar[4])
					tar[1] = int(y1)
					tar[2] = int(y2)
					tar[3] = int(y3)
					tar[4] = int(y4)
				if tar[5] == 1:
					tar[1] += int(y1)
					tar[2] += int(y2)
					tar[3] += int(y3)
					tar[4] += int(y4)
	xar.append(tar[0])
	y1ar.append(tar[1])
	y2ar.append(tar[2])
	y3ar.append(tar[3])
	y4ar.append(tar[4])
	xar = [x for x in range(0, len(y1ar))]
	ax1.clear()
	ax1.plot(xar,y1ar,label='$news$',color='red',linewidth=1)
	ax1.plot(xar,y2ar,label='$comm$',color='blue',linewidth=1)
	ax1.plot(xar,y3ar,label='$memes$',color='green',linewidth=1)
	ax1.plot(xar,y4ar,label='$ongoing$',color='orange',linewidth=1)
	ax1.set_title("Categories Map")
	ax1.legend(loc='upper right',prop={'size':10})
	ax1.set_xlabel("Time")
	ax1.set_ylabel("Numbers")

ani = animation.FuncAnimation(fig,animate, interval=1000)
plt.show()