__author__ = 'anirudha'
import matplotlib.pyplot as plt
import pickle
from __init__ import file_name

file = open(file_name,'rb')
object_file = pickle.load(file)
fitness_data = object_file[2][:]
file.close()
print(fitness_data[0])
print(object_file[0][0][:])
print(object_file[1][:])
#print(fitness_data[1])
#print(fitness_data[2])
for i in range(4):
    plt.plot(object_file[0][0][i*20:(i+1)*20-1])
plt.show()
