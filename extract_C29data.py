import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    
    return array[idx]

#Simple mouse click function to store coordinates
def onclick1(event):
    global ix
    ix = event.xdata

    #assign global variable to access outside of function
    global coords
    coords.append(ix)
    
    #Disconnect after 2 clicks
    if len(coords) == 2:
        fig1.canvas.mpl_disconnect(cid1)
        plt.close()
    return

path = '/home/geraldfj/Documents/python/ToPing/area_data'

data = np.array(pd.read_csv(path, sep = ',', header = None).dropna(axis='columns'))
time = data[0]
abund = data[1]


fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

ax1.grid(True)
ax1.plot(time,abund,color='g')
    
coords = []
cid1 = fig1.canvas.mpl_connect('button_press_event',onclick1)
manager = plt.get_current_fig_manager()

plt.show()
plt.close(fig1)


t_left = find_nearest(time,coords[0])
t_right = find_nearest(time,coords[1])
      
y_left = abund[time.tolist().index(t_left)]
y_right = abund[time.tolist().index(t_right)]

print(t_left,y_left)
print(t_right,y_right)


