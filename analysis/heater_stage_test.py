"""
Test data analysis and plotting of first self-made heater stage test

Check TestChamber Labnotebook entry (04/28/19) for description of test 


date:   04/27/2019
"""
__author__ = "kha"
__version__ = "1.0.0"


import numpy as np
import matplotlib.pyplot as plt




### Data

V = np.array([0.7,1.1,0.9,1.0,1.3,1.4,1.6,1.8,1.9,2.2,2.5])   # [V]
I = np.array([0.5,1.0,1.5,2.5,3.0,3.5,4.0,4.5,5.5,6.5])       # [A]
T = np.array([28,33,35,39,43,50,71,81,110,129,150])       # [°C]


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
ax2.plot(V,T, c='orange')
plt.grid()


plt.show()
