""" 
Test SM70-22 power supply V-monitor and I-monitor pins at 15pin D-Sub 
connector on the backside

date = 05/09/2019
"""



import numpy as np
import matplotlib.pyplot as plt


I_set = [
	0.4,
	1.0,
	2.0,
	3.0,
	4.0,
]

V_set = [
	1.0,
	1.8,
	2.7,
	3.0,
	3.4
]

I_pin = [
	0.112,
	0.246,
	0.470,
	0.695,
	0.928
]

V_pin = [
	0.071,
	0.127,
	0.191,
	0.217,
	0.249
]


ax1_dct = {
	'xlabel':	'I_set',
	'ylabel':	'I_pin',
}

fig1 = plt.figure(figsize=(6,4))
ax1 = fig1.add_subplot(111, **ax1_dct)
ax1.plot(I_set, I_pin)
plt.grid()


ax2_dct = {
	'xlabel':	'V_set',
	'ylabel':	'V_pin',
}

fig2 = plt.figure(figsize=(6,4))
ax2 = fig2.add_subplot(111, **ax2_dct)
ax2.plot(I_set, I_pin)
plt.grid()


plt.show()