import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.ndimage import gaussian_filter1d, maximum_filter1d

data = pd.read_csv('ciwan_1.txt', sep='\t', header=None, names=range(8))

acceleration = data[data[1] == 'ACC'][[0,2,3,4]].to_numpy()

print(acceleration)

start_time = acceleration[0,0]/1000
time = acceleration[:,0]/1000 - start_time
magnitude = np.abs(np.sqrt(np.sum(acceleration[:,1:4]**2, 1)) - 9.81)

# smooth the data
max_magnitude = maximum_filter1d(magnitude, 100)
max_smooth_magnitude = gaussian_filter1d(maximum_filter1d(magnitude, 50), 100)
smoothed_magnitude = gaussian_filter1d(magnitude, 100)

plt.plot(time, magnitude)
plt.plot(time, smoothed_magnitude, label='smoothed')
plt.plot(time, max_magnitude, label='max')
plt.plot(time, max_smooth_magnitude, label='max smooth')
# plt.plot(acceleration[:,0]/1000 - start_time, np.abs(acceleration[:,1]), label='x')
# plt.plot(acceleration[:,0]/1000 - start_time, np.abs(acceleration[:,2]), label='y')
# plt.plot(acceleration[:,0]/1000 - start_time, np.abs(acceleration[:,3]), label='z')
# plt.plot(acceleration[:,0]/1000 - start_time, np.sqrt(np.sum(acceleration[:,1:4]**2, 1)), label='l2')
plt.show()


# threshold
running_threshold = 20
walking_threshold = 5
time_threshold = 10

current_state = None
start = 0
fig, ax = plt.subplots()

for t, data in zip(time, max_smooth_magnitude):
    if data > running_threshold:
        new_state = 'running'
    elif data > walking_threshold:
        new_state = 'walking'
    else:
        new_state = 'sitting'

    if new_state != current_state and current_state is not None:
        if t - start >= time_threshold:
            if current_state == 'sitting':
                ax.axvspan(start, t, alpha=0.5, color='green')
            if current_state == 'walking':
                ax.axvspan(start, t, alpha=0.5, color='yellow')
            if current_state == 'running':
                ax.axvspan(start, t, alpha=0.5, color='red')
            start = t
        
    current_state = new_state

if current_state == 'sitting':
    ax.axvspan(start, t, alpha=0.5, color='green')
    
if current_state == 'walking':
    ax.axvspan(start, t, alpha=0.5, color='yellow')
if current_state == 'running':
    ax.axvspan(start, t, alpha=0.5, color='red')


green_patch = mpatches.Patch(color='green', label='Stand still')
yellow_patch = mpatches.Patch(color='yellow', label='Walking')
red_patch = mpatches.Patch(color='red', label='Running')
plt.legend(handles=[green_patch, yellow_patch, red_patch])

plt.plot(time, max_smooth_magnitude, label='max smooth')
plt.show()