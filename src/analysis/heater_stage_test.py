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
t = np.array([	# [min]





])
I = np.array([	# [A]
	0.5,
	1.0,
	1.5,
	2.0,
	2.5,
	3.0,
	3.5,
	4.0,
	4.5,
	5.5,
	6.5,
	7.5,
	8.5,
	10,
	12
])
V = np.array([	# [V]
	0.7,
	1.1,
	0.9,
	1.0,
	1.3,
	1.4,
	1.6,
	1.8,
	1.9,
	2.2,
	2.5,
	2.8,
	3.1,
	3.6,
	4.3
])
T = np.array([	# [°C]
	28,
	33,
	35,
	39,
	43,
	50,
	71,
	81,
	110,
	129,
	150,
	173,
	190,
	224,
	260
])


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
