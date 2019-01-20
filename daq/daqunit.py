"""
DAQ unit control class



TODO:
1. write mocking class for u6. Necessary to develop code without being dependent 
on hardware connected. need to mock

* open in U6 and DEvice
* _writeRead in U6
* write() in U6
* read() in U6

"""
__version__ = "0.0.1"
__author__ = "kha"


import u6



# ==============================================================================
# DAQUnitError class
# ==============================================================================
class DAQUnitError(Exception):
	""" """
	pass


class DAQUnitExceptionHandling(object):
	""" """

	def check_pin_config_type(self, pin_config):
		"""checks if pin_config variable is of type dictionar"""
		if type(pin_config) != dict:
			raise DAQUnitError('pin_config variable must be of type dict')
		return



# ==============================================================================
# DAQUnit class
# ==============================================================================
class DAQUnitBase(DAQUnitExceptionHandling):
	""" """

	def __init__(self, pin_config={}, pin_settings={}, **kwargs):
		""" """
#		self.check_pin_config_type(pin_config)
		self.pc = pin_config
		self.ps = pin_settings

#		self.setup_daq(**kwargs)


	def setup_daq(self, **kwargs):
		"""builds up communication with U6 hardware"""
		self.d = u6.U6(**kwargs)


	def init_channel_objects(self):
		""" """
		# self.p = {}
		# keys = self.pc.keys()

		# u6.AIN24AR(self.pc[key])
		pass

	def init_channel(self):
		""" """
		pass


	def get_pressure(self):
		""" """
		positiveChannel = ai_dct[self.pc['pressure']]
#		kwargs = self.ps
#		return self.d.getAIN(positivechannel, **kwargs)





# U6 channel name mapping
dio_dct = {
    'FIO0':		0,
    'FIO1':		1,
    'FIO2':		2,
    'FIO3':		3,
    'FIO4':		4,
    'FIO5':		5,
    'FIO6':		6,
    'FIO7':		7,
    'EIO0':		8,
    'EIO1':		9,
    'EIO2':		10,
    'EIO3':		11,
    'EIO4':		12,
    'EIO5':		13,
    'EIO6':		14,
    'EIO7':		15,
    'CIO0':		16,
    'CIO1':		17,
    'CIO2':		18,
    'CIO3':		19,
    'MIO0':		20,
    'MIO1':		21,
    'MIO2':		22,
}

ai_dct = {
	'AI0':		0,
	'AI1':		1,
	'AI2':		2,
	'AI3':		3,
	'AI4':		4,
	'AI5':		5,
	'AI6':		6,
	'AI7':		7,
	'AI8':		8,
	'AI9':		9,
	'AI10':		10,
	'AI11':		11,
	'AI12':		12,
	'AI13':		13,
}

ao_dct = {
	'AO0':		0,
	'AO1':		1,
}

# pin configuration example
#	this dct contains the information to which AI the different input signals
#	are connected. 
pin_config_ex = {
	'pressure':			'AI0',
	'TC1':				'AI1',
	'TC2':				'AI2',
	'TP_remote':		'FIO0',		# DO
	'TP_power':			'FIO1',		# DO
	'TP_valve':			'FIO2',		# DO
	'filament_on':		'FIO3',		# DI
}

pin_settings = {
	'pressure':		{ResolutionIndex=0, GainIndex=0, SettlingFactor=0, Differential=False},
	'TC1':			{},
	'TC2':			{},
#	'TP_remote':	{},
#	'TP_power':		{},
#	'TP_valve':		{},
}





# ==============================================================================
# main
# ==============================================================================
if __name__ == "__main__":
	print('hello DAQUnit')
	pass



