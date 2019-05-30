

import csv
import sys
import math
import matplotlib
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd



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

#Ts start & end times = 39.337 & 39.622
#Tm start & end times = 39.958 & 40.345
#C29 start & end times = 41.033 & 41.380
#C30 start & end times = 41.683 & 42.326
#C31S,R start & end times = 42.825 & 43.446
#C32S,R start & end times = 43.496 & 44.297
#C33S,R start & end times = 44.437 & 45.288 
#C34S,R start & end times = 45.433 & 46.234
#C30bb start & end times = 43.496 & 44.297

start_time = 39.135
end_time = 46.357
C30_start_time = 39.337
C30_end_time = 39.622
hC30_1_est = []
scan_hC30_1_est = []
condition_array = []


path1 = '/home/geraldfj/Documents/python/Project4/Target.txt'
path2 = '/home/geraldfj/Documents/python/Project4/XWarped.txt'
path3 = '/home/geraldfj/Documents/python/Project4/data1.csv'


target = np.array(pd.read_csv(path1,sep = ' ',header = None))
xwarped = np.array(pd.read_csv(path2,sep = ' ',header = None))


df = pd.read_csv(path3,sep=';')
df['RT(minutes) - NOT USED BY IMPORT'] = df['RT(minutes) - NOT USED BY IMPORT'].round(3)
data = np.array(df[['RT(minutes) - NOT USED BY IMPORT','191']].values.tolist())
label = np.array(list(df.columns.values))


timet = np.array(data[:,0])

#selecting the index values between the selected times
start_point = timet.tolist().index(start_time)
end_point = timet.tolist().index(end_time)
t = np.array(timet[start_point:end_point])

#change from Matlab's 1Xn array to n shape array
target = target.reshape(-1)
target = np.array(target[1:target.shape[0]])

xwarped = np.array(xwarped[:,1:xwarped.shape[1]])

#combine target and warped data into one single dataset
h_exp = np.concatenate((target.reshape(1,target.shape[0]),xwarped),axis = 0)

################################################################
#From this onwards, the code focus on C30hopane data####
###############################################################3

C30_start = t.tolist().index(C30_start_time)
C30_end = t.tolist().index(C30_end_time)

t_C30 = np.array(t[C30_start:C30_end])
h_exp_C30 = np.array(h_exp[:,C30_start:C30_end])


y_left = []
y_right = []
x1 = []
x2_start = []
x3_start = []
x2_end = []
x3_end = []



for i in range(h_exp_C30.shape[0]):
    # Values estimated by program
    HR = np.amax(h_exp_C30[i])  #maximum abundance
    TR = t_C30[h_exp_C30[i].tolist().index(HR)] #time at max abundance
    diff = np.diff(h_exp_C30[i])    #est first derivative
    diff_max = diff.tolist().index(np.amax(diff))   #max of derivative value
    diff_min = diff.tolist().index(np.amin(diff))   #min of derivative value

    #to get starting point of chromatogram
    for j in range((diff_max-1),-1,-1):
        if diff[j] <= 0:
            start = j
            break
    #to get ending point of chromatogram
    for j in range(diff_min,h_exp_C30[i].shape[0]):
        if diff[j] >= 0:
            end = j
            break
        
    tR_start = t_C30[start] #start time of chromatogram
    tR_end = t_C30[end]     #end time of chromatogram

    #User inputs for start and end times of chromatographic peak
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.set_xlabel("Time (mins)")
    ax1.set_ylabel("Abundance")
    ax1.set_title("Plot of Data "+str(i+1))
    ax1.grid(True)
    ax1.plot(t_C30,h_exp_C30[i],color='g')
    
    coords = []
    cid1 = fig1.canvas.mpl_connect('button_press_event',onclick1)
    plt.show()
    plt.close(fig1)


######## y values ##################
    t_left = find_nearest(t_C30,coords[0])
    t_right = find_nearest(t_C30,coords[1])
      
    y_left.append([t_left,h_exp_C30[i][t_C30.tolist().index(t_left)]])
    y_right.append([t_right,h_exp_C30[i][t_C30.tolist().index(t_right)]])

######## x values ###################

    tR_diff_start = abs(tR_start-TR)
    tR_diff_end = abs(tR_end-TR)
    x1.append([TR,HR])  #time&abundance at RT

    #parameters for start values
    x2_start.append([tR_start,h_exp_C30[i][t_C30.tolist().index(tR_start)]])
    x3_start.append(tR_diff_start)

    #parameters for end values
    x2_end.append([tR_end,h_exp_C30[i][t_C30.tolist().index(tR_end)]])
    x3_end.append(tR_diff_end)
        
       
y_left = np.array(y_left)
y_right = np.array(y_right)
x1 = np.array(x1)
x2_start = np.array(x2_start)
x2_end = np.array(x2_end)
x3_start = np.array(x3_start)
x3_end = np.array(x3_end)



textfile = open('/home/geraldfj/Documents/python/LR_ML1/y_Ts_data','w')
textfile.close()

textfile = open('/home/geraldfj/Documents/python/LR_ML1/X_Ts_data','w')
textfile.close()



for i in range(y_left.shape[0]):
    textfile = open('/home/geraldfj/Documents/python/LR_ML1/y_Ts_data','a')
    textfile.write(str(y_left[i][0]) + ',' + str(y_left[i][1]) + ',' + str(y_right[i][0]) + ',' + str(y_right[i][1]) +'\n')
    textfile.close()



for i in range(x1.shape[0]):
    textfile = open('/home/geraldfj/Documents/python/LR_ML1/X_Ts_data','a')
    textfile.write(str(x1[i][0]) + ',' + str(x1[i][1]) + ',' + str(x2_start[i][0]) + ',' + str(x2_start[i][1]) + ',' + str(x3_start[i]) + ',' + str(x2_end[i][0]) + ',' + str(x2_end[i][1]) + ',' + str(x3_end[i]) + '\n')
    textfile.close()



    



    
