""" 



"""
__author__ = "kha"
__version__ = "0.0.1"


import u6
import math



# d = u6.U6()
# d.configU6()

# channel 			= 0
# resolutionIndex 	= 1
# gainIndex 		= 0
# settlingFactor 	= 0
# differential 		= False

# cmd 				= u6.AIN24AR(channel, resolutionIndex, gainIndex, settlingFactor, differential)
# reading = d.getFeedback(cmd)
# volt = d.binaryToCalibratedAnalogVoltage(gainIndex, reading[0]['AIN'])
# d.close()


class U6Reader(object):
	""" """

	AIN24AR_SETTINGS = {
		'ResolutionInex':	0,
		'GainIndex':		0,
		'SettlingFactor':	0,
		'Differential':		False
	}

	def __init__(self, d, channel, **kwargs):
		""" """
		self.settings = U6Reader.AIN24AR_SETTINGS
		self.settings.update(kwargs)
		self.cmd = u6.AIN24AR(channel, **kwargs)
		self.d = d

	def get_reading(self):
		""" """
		reading = self.d.getFeedback(self.cmd)
		volt = self.d.binaryToCalibratedAnalogVoltage(self.settings['GainIndex'], reading[0]['AIN'])
		return volt


#class PKR251Base(object):
#	""" """
#
#	d = {
#		'mbar':	11.33,
#		'torr': 11.46,
#		'Pa':	9.333,
#		'kPa':	12.33	
#	}
#
#	def __init__(self, *args, **kwargs):
#		""" """
#		super().__init__(*args, **kwargs)


# ==============================================================================
# Excpetion class
# ==============================================================================

class PKR251Exception(Exception):
	"""Exception class for  """
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


# ==============================================================================
# PKR251 class
# ==============================================================================

class PKR251(U6Reader):
	"""Class object to represent PKR251 pressure gauge

	Class object is derived from **U6Reader** object since PK251 gauge 
	is interfaced by Labjack U6

	:param d: U6 Labjack DAQ Unit 
	:type d: u6.U6

	"""

	D = {
		'mbar':	11.33,
		'torr': 11.46,
		'Pa':	9.333,
		'kPa':	12.33	
	}

	def __init__(self, d, channel=0, *args, **kwargs):
		super().__init__(d, channel, *args, **kwargs)
		self.p_unit = 'mbar'

	def get_pressure(self, p_unit=None):
		if p_unit == None: p_unit = self.p_unit
		volt = self.get_reading()
		return PKR251.voltage_to_pressure(volt, p_unit)


	@staticmethod
	def voltage_to_pressure(u, p_unit='mbar'):
		""" """
		if not p_unit in PKR251.D.keys():
			raise PKR251Exception(
				"p_unit variable needs to be element of {:s}".format(str(list(PKR251.D.keys())))
				)

		p = PKR251.conversion_formula(u, PKR251.D[p_unit])
		return p

	@staticmethod
	def conversion_formula(u,D):
		"""conversion formula from Pfeiffer PKR251 manual"""
		return 10**(1.667*u-D)


# ==============================================================================
# main
# ==============================================================================

def record_pressure_trace(time_interval=600):
	""" """
	import time


	d = u6.U6()
	d.configU6()
	pkr = PKR251(d)

	pressure = []
	t = []

	t0 = time.time()
	for i in range(time_interval):
		pressure.append(pkr.get_pressure('torr'))
		t.append(time.time()-t0)
		time.sleep(1)
		print('time: {0:.2f}s; pressure: {1:2e}torr'.format(t[-1], pressure[-1]))

	return t, pressure

# ==============================================================================
# main
# ==============================================================================

if __name__ == "__main__":
	d = u6.U6()
	d.configU6()
	pkr = PKR251(d)
	pkr.get_pressure()

