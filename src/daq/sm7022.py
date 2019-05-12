"""
Class definition to controla Delta Electonika SM70-22 DC Power supply with 
two analog inputs and one analog output of a Labjack U6. Interface used 
for this is the Analog programmable connection specified in the user manual.


https://www.delta-elektronika.nl/upload/PRODUCT_MANUAL_SM1500_V201808.pdf


date = 05/09/2019
"""

__version__ = "1.0.0"
__author__ = "kha"


from .daqunit import AI_channel ,AO_channel


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




class SM7022(AI_channel, AO_channel):
	""" """

	V_READOUT_MAX 	= 5.0	# [V]
	V_OUTPUT_MAX 	= 70	# [V]
	I_OUTPUT_MAX	= 22 	# [A]

	def __init__(self, *args, **kwargs):
		""" """
		super().__init__(*args, **kwargs)
		if 'pin_config' not in kwargs.keys():
			self.pin_config = PIN_CONFIG

	def get_voltage(self):
		""" """
		volt = self.get_ai_value('V_monitor')
		return SM7022.convert_to_volt_output(volt)

	def get_current(self):
		""" """
		volt = self.get_ai_value('I_monitor')
		return SM7022.convert_to_current_output(volt)

	def set_current(self, current):
		""" """
		volt = SM7022.convert_to_readout_voltage(current)
		self.set_ao('I_program', volt)


	@staticmethod
	def convert_to_volt_output(volt_readout):
		""" """
		return volt_readout / SM7022.V_READOUT_MAX * SM7022.V_OUTPUT_MAX

	@staticmethod
	def convert_to_current_output(volt_readout):
		""" """
		return volt_readout / SM7022.V_READOUT_MAX * SM7022.I_OUTPUT_MAX

	@staticmethod
	def convert_to_readout_voltage(current):
		return current / SM7022.I_OUTPUT_MAX * SM7022.V_READOUT_MAX





