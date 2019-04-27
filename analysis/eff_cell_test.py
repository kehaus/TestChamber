"""
Test data and analysis for self-made effusion cell performance


date:   04/18/2019
"""
__author__ = "kha"
__version__ = "1.0.1"


import numpy as np
import matplotlib.pyplot as plt




### Data

V = np.array([0.1,0.2,0.3,0.5,0.8,1.0,1.2,1.5,1.7,1.9,2.1,2.6, 3.1])   # [V]
I = np.array([0.5,1.0,1.5,2.5,4.0,5.0,6.0,7.0,8.0,9.0,10,12,14])     # [A]
T = np.array([23,26,31,44,84,132,180,233,296,350,407, 506, 611])       # [°C]


### plot results
ax1_dct = {
  'xlabel':   'Current I [A]',
  'ylabel':   'Temperature T [°C]'
}

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, **ax1_dct)
ax1.plot(I,T)
plt.grid()

ax2_dct = {
  'xlabel': 'Current I [A]',
  'ylabel': 'Voltage V [V]'
}

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, **ax2_dct)
ax2.plot(I,V, c='orange')
plt.grid()


plt.show()




