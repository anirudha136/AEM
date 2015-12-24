__author__ = 'anirudha'
import csv
import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def init():
    return line,

def update(num):
    #newData = np.array([[1 + num, 2 + num / 2, 3, 4 - num / 4, 5 + num],[7, 4, 9 + num / 3, 2, 3]])
    newData = np.vstack((range(num),data[:num]))
    #print(newData)
    line.set_data(newData)
    # This is not working i 1.2.1
    # annotation.set_position((newData[0][0], newData[1][0]))

with open('result.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    i = 0
    data = []
    for row in spamreader:
        #print ', '.join(row)
        try:
            if i>0:
                data.append(int(row[1]))
            i = i+1
        except ValueError:
            pass
    #data = np.array([[range(len(data))],[data]])
print(data)
fig = plt.figure()
ax = plt.axes(xlim=(0, len(data)), ylim=(0, 50000))
line, = ax.plot([], [], 'r-')
anim = animation.FuncAnimation(fig, update, frames=len(data), init_func=init,interval=20, blit=False)
    #anim.save('im.mp4', writer=writer)
plt.show()
    #plt.plot(data)
