""" 



"""
__author__ = "kha"
__version__ = "0.0.1"


import u6
import math



PIN_CONFIG = {		# PKR251 manual p.11
	'identification':	'PKR251_1',
	'signal_output':	'PKR251_2',
	'signal_common':	'PKR251_3',
	'supply':			'PKR251_4',
	'supply_common':	'PKR251_5',
	'screen':			'PKR251_6'
}

DEFAULT_P_UNIT = 'torr'

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

class PKR251(object):
	"""Class object to represent PKR251 pressure gauge

	Class object is derived from **U6Reader** object since PK251 gauge 
	is interfaced by Labjack U6

	:param dd: TestChamber DAQUnit
	:type dd: src.daq.daqunit.DAQUnitBase

	"""

	D = {
		'mbar':	11.33,
		'torr': 11.46,
		'Pa':	9.333,
		'kPa':	12.33	
	}

	def __init__(self, dd, channel=0, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.dd = dd
		self.pin_config = PIN_CONFIG
		self.p_unit = DEFAULT_P_UNIT

	def get_pressure(self, p_unit=None):
		if p_unit == None: p_unit = self.p_unit

		volt = self.dd.get_ai_value(
			self.get_u6_pin_name('signal_output'))
		return PKR251.voltage_to_pressure(volt, p_unit)

	def get_u6_pin_name(self, pkr_pin_name):
		"""converts PKR251 pin convenction to U6 pin convention

		''pkr_pin_name'' can be a string or a nested list of strings

		"""
		if type(pkr_pin_name) is list:
			return [self.get_u6_pin_name(x) for x in pkr_pin_name]
		self._check_pin_name(pkr_pin_name)
		u6_pin_name = self.dd.pc[self.pin_config[pkr_pin_name]]
		return u6_pin_name

	def _check_pin_name(self, pin_name):
		"""checks if pin name is in self.pin_config"""
		if pin_name not in self.pin_config.keys():
			raise PKR251Exception('pin_name not known. Not part of pin_config')
		return

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
# record pressure trace
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
#	d = u6.U6()
#	d.configU6()
#	pkr = PKR251(d)
#	pkr.get_pressure()
	pass
