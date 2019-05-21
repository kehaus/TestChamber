"""
Class definition to controla Delta Electonika SM70-22 DC Power supply with 
two analog inputs and one analog output of a Labjack U6. Interface used 
for this is the Analog programmable connection specified in the user manual.


https://www.delta-elektronika.nl/upload/PRODUCT_MANUAL_SM1500_V201808.pdf


date = 05/09/2019
"""

__version__ = "1.1.0"
__author__ = "kha"


from .daqunit import AI_channel ,AO_channel
from .tc import TC






class DEPowerSupply(AI_channel, AO_channel):
	"""represents DELTA ELEKTRONIKA DC Power supplies

	"""

	V_READOUT_MAX 	= None		# [V]
	V_OUTPUT_MAX 	= None		# [V]
	I_OUTPUT_MAX	= None		# [A]


	def __init__(self, *args, **kwargs):
		""" """
		super().__init__(*args, **kwargs)
		if 'pin_config' not in kwargs.keys():
			self.pin_config = self.PIN_CONFIG.copy()

	def get_voltage(self):
		""" """
		volt = self.get_ai_value('V_monitor')
		return self.convert_to_volt_output(volt)

	def get_current(self):
		""" """
		volt = self.get_ai_value('I_monitor')
		return self.convert_to_current_output(volt)

	def set_current(self, current, verbose=False):
		""" """
		if verbose:
			print('SM7022 set current to {:.2f}'.format(current))
		volt = self.convert_to_readout_voltage(current)
		self.set_ao('I_program', volt)


	@classmethod
	def convert_to_volt_output(cls, volt_readout):
		""" """
		return volt_readout / cls.V_READOUT_MAX * cls.V_OUTPUT_MAX

	@classmethod
	def convert_to_current_output(cls, volt_readout):
		""" """
		return volt_readout / cls.V_READOUT_MAX * cls.I_OUTPUT_MAX

	@classmethod
	def convert_to_readout_voltage(cls, current, correction_factor=0.1):
		""" 
		correction factor is necessary because current value entered here does not 
		atual output current on DC power supply.


		"""
		return current / cls.I_OUTPUT_MAX * cls.V_READOUT_MAX * (1+correction_factor)



class ES03010(DEPowerSupply):
	"""Represents the ES 300 Series 300Watts DC power supplies


	Example:
		>>> dd = DAQUnitBase()
		>>> es = ES03010(dd)
		>>> es.get_current()
		>>> es.get_voltage()
		>>> es.set_current(1)


	"""

	V_READOUT_MAX 	= 5.0	# [V]
	V_OUTPUT_MAX 	= 30	# [V]
	I_OUTPUT_MAX	= 10	# [A]


	PIN_CONFIG = {
		'0ref_prog':	'ES030_1',
		'I_monitor':	'ES030_2',
		'I_program':	'ES030_3',
		'CC_status':	'ES030_4',
		'RSD':			'ES030_5',
		'plus12V':		'ES030_7',
		'stat_12V':		'ES030_8',
		'Ref5_1V':		'ES030_9',
		'V_monitor':	'ES030_10',
		'V_program':	'ES030_11'
	}


class SM7022(DEPowerSupply):
	"""Represents the SM1500 Series. 1500 Watts power supplies


	"""

	V_READOUT_MAX 	= 5.0	# [V]
	V_OUTPUT_MAX 	= 70	# [V]
	I_OUTPUT_MAX	= 22 	# [A]

	PIN_CONFIG = {
		'0ref_prog':	'SM7022_1',
		'I_monitor':	'SM7022_2',
		'I_program':	'SM7022_3',
		'CC_status':	'SM7022_4',
		'RSD':			'SM7022_5',
		'plus12V':		'SM7022_7',
		'stat_12V':		'SM7022_8',
		'Ref5_1V':		'SM7022_9',
		'V_monitor':	'SM7022_10',
		'V_program':	'SM7022_11',
		'OT_status':	'SM7022_12',
		'LIM_status':	'SM7022_13',
		'DCF_status':	'SM7022_14',
		'ACF_status':	'SM7022_15'
	}


	# def __init__(self, *args, **kwargs):
	# 	""" """
	# 	super().__init__(*args, **kwargs)
	# 	if 'pin_config' not in kwargs.keys():
	# 		self.pin_config = self.PIN_CONFIG.copy()



class HeaterStage(SM7022):
	""" """

	PIN_CONFIG_HS = {
		'chromel':	'HSTC_CH',
		'alumel':	'HSTC_AL'
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tc = TC(self.dd, pin_config=HeaterStage.PIN_CONFIG_HS)

	def get_temperature(self, *args, **kwargs):
		return self.tc.get_temperature(*args, **kwargs)



class EffusionCell(ES03010):
	""" """

	PIN_CONFIG_EF = {
		'chromel':	'EFTC_CH',
		'alumel':	'EFTC_AL'
	}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.tc = TC(self.dd, pin_config=EffusionCell.PIN_CONFIG_EF)

	def get_temperature(self, *args, **kwargs):
		return self.tc.get_temperature(*args, **kwargs)

