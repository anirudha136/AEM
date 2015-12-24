import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
temp = np.random.rand(10)
line, = ax.plot(temp)
ax.set_ylim(0, 1)

def update(data,temp):
    temp = temp[1:9]
    data = np.append(temp,data)
    line.set_ydata(data)
    return line,

def data_gen():
    while True:
        a = np.random.rand(1)
        yield a

ani = animation.FuncAnimation(fig, update, data_gen ,interval=1000)
plt.show()
