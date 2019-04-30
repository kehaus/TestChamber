"""
Test data analysis and plotting of first precursor inlet test

Check TestChamber Labnotebook entry (04/29/19) for description of test 


date:   04/29/2019
"""
__author__ = "kha"
__version__ = "1.0.0"


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt



### measurement data
valve_pos_open = np.array([
	0,
	50,
	100,
	120,
	140,
	170,
	190,
	210,
	250,
	300,
	350,
])
valve_pos_close = np.array([
	350,
	250,
	200,
	150,
	130,
	110,
	90,
	60,
	40
])

p_open = np.array([		# [torr]
	2.1,
	2.1,
	2.1,
	2.4,
	3.0,
	9.5,
	11,
	12,
	12,
	12,
	12
]) * 10**-7
p_close = np.array([	# [torr]
	12,
	12,
	12,
	5.7,
	3.1,
	2.6,
	2.1,
	2.1,
	2.0
]) * 10**-7



### plot results
ax1_dct = {
  'xlabel':   'needle valve position [valve scale]',
  'ylabel':   'Pressure [torr]'
}

fig1 = plt.figure(figsize=(8,5))
ax1 = fig1.add_subplot(111, **ax1_dct)
ax1.plot(valve_pos_open,p_open, label='open valve')
ax1.plot(valve_pos_close, p_close, label='close valve')
ax1.legend(loc=0)
ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.1e}'))
plt.grid()


#ax2_dct = {
#  'xlabel': 'Current I [A]',
#  'ylabel': 'Voltage V [V]'
#}

#fig2 = plt.figure()
#ax2 = fig2.add_subplot(111, **ax2_dct)
#ax2.plot(I,V, c='orange')


plt.show()

