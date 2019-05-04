"""
Test data analysis and plotting of freshly filled eff cell 

Check TestChamber Labnotebook entry (04/30/19) for description of test 


date:   04/30/2019
"""
__author__ = "kha"
__version__ = "1.0.0"


import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


from ..util.import_handle import DATA_PATH


# bug fix to make it work when runned from command line
__path__ = os.getcwd()
 
# =====================================
# Measurement Data
# =====================================
data_fn = os.path.join(DATA_PATH, "eff_cell_with_Te_test.txt")

df = pd.read_csv(data_fn, sep='\t')


ax1_dct = {
	'xlabel':	'Current  [A]',
	'ylabel':	'Temperature [C]'
}

fig1 = plt.figure(figsize=(10,6))
ax1 = fig1.add_subplot(111, **ax1_dct)
ax1.plot(df['I [A]'][:-2], df['T [C]'][:-2])
plt.grid()

ax2_dct = {
	'xlabel':	'Temperature [C]',
	'ylabel':	'pressure [torr]',
}

fig2 = plt.figure(figsize=(10,6))
ax2 = fig2.add_subplot(111, **ax2_dct)
ax2.plot(df['T [C]'][:-2], df['p [torr]'][:-2])
plt.grid()


plt.show()


