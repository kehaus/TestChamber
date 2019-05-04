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



# ====================================
# measurement data
# ====================================

## precursor temperature 22°C
valve_pos_open_22C = np.array([
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
valve_pos_close_22C = np.array([
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

p_open_22C = np.array([		# [torr]
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
p_close_22C = np.array([	# [torr]
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


## precursor temperature 50°C
valve_pos_open_50C = np.array([
	0,
	20,
	40,
	60,
	80,
	100,
	120,
	140,
	160,
	180,
	200,
	220,
	240,
	260,
	280,
	300
])


valve_pos_close_50C = np.array([
	300,
	250,
	200,
	150,
	100,
	50,
	0
])

p_open_50C = np.array([		# [torr]
	0.34,
	0.34,
	0.34,
	0.36,
	0.41,
	0.63,
	1.0,
	1.7,
	6.9,
	11,
	12,
	13,
	14,
	14,
	14,
	14
]) * 10**-7

p_close_50C = np.array([		# [torr]
	14,
	14,
	13,
	4.4,
	0.7,
	0.58,
	0.45
]) * 10**-7



## precursor temperature 77°C
valve_pos_open_77C = np.array([
	0,
	20,
	40,
	60,
	80,
	100,
	120,
	140,
	160,
	180,
	200,
	220,
	240,
	260,
	280,
	300
])


valve_pos_close_77C = np.array([
	300,
	250,
	200,
	150,
	100,
	50,
	0
])

p_open_77C = np.array([		# [torr]
	0.33,
	0.32,
	0.33,
	0.33,
	0.40,
	0.65,
	1.2,
	2.4,
	9.3,
	14,
	17,
	17,
	18,
	18,
	18,
	18
]) * 10**-7

p_close_77C = np.array([		# [torr]
	18,
	18,
	17,
	5.6,
	0.47,
	0.38,
	0.36
]) * 10**-7


# ====================================
# plots
# ====================================
ax1_dct = {
  'xlabel':   'Needle valve position [valve scale]',
  'ylabel':   'Pressure [torr]'
}

fig1 = plt.figure(figsize=(8,5))
ax1 = fig1.add_subplot(111, **ax1_dct)
ax1.plot(valve_pos_open_22C,p_open_22C, label='open valve')
ax1.plot(valve_pos_close_22C, p_close_22C, label='close valve')
ax1.legend(loc=0)
ax1.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.1e}'))
plt.grid()


ax2_dct = {
  'xlabel':     'Needle valve position [valve scale]',
  'ylabel':     'Pressure [torr]',
  'ylim':		[1*10**-8, 2*10**-6],
#  'yscale':		'log',
}

fig2 = plt.figure(figsize=(8,5))
ax2 = fig2.add_subplot(111, **ax2_dct)
ax2.plot(valve_pos_open_22C,p_open_22C, label='open valve 22C')
ax2.plot(valve_pos_close_22C, p_close_22C, label='close valve 22C')
ax2.plot(valve_pos_open_50C,p_open_50C, label='open valve, 50C')
ax2.plot(valve_pos_close_50C, p_close_50C, label='close valve 50C')
ax2.plot(valve_pos_open_77C,p_open_77C, label='open valve 77C')
ax2.plot(valve_pos_close_77C, p_close_77C, label='close vale, 77C')
ax2.legend(loc=0)
ax2.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:.1e}'))
#ax2.set_yscale('log')
plt.grid()

plt.show()

