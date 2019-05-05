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
import time




PIN_CONFIG = {	# schematics of what is connected to U6
	5:		'FIO0',
	'E':	'FIO1',
	6:		'FIO2',
	'F':	'FIO3',
	7:		'FIO4',
	'H':	'FIO5',
}

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

	def __init__(self, pin_config=None, pin_settings={}, **kwargs):
		""" """
#		self.check_pin_config_type(pin_config)
		self.setup_daq()

		if pin_config is None: self.pc = PIN_CONFIG
		self.ps = pin_settings
		self.dio_dct = DIO_DCT
		self.ai_dct = AI_DCT
		self.AO_DCT = AO_DCT
		pass

	def setup_daq(self, **kwargs):
		"""builds up communication with U6 hardware"""
		self.d = u6.U6(**kwargs)
		self.config = self.d.configU6()


	def init_channel_objects(self):
		""" """
		# self.p = {}
		# keys = self.pc.keys()

		# u6.AIN24AR(self.pc[key])
		pass

	def init_channel(self):
		""" """
		### set up DIO as correct in and output channel 

		pass


#	def get_pressure(self):
#		""" """
#		positiveChannel = ai_dct[self.pc['pressure']]
#		kwargs = self.ps
#		return self.d.getAIN(positivechannel, **kwargs)
	def get_dio_state(self, channel):
		channel = self._check_dio_channel_input(channel)
		rtn = self.d.getFeedback(u6.BitStateRead(channel))
		return rtn[0]

	def set_dio_state(self,channel, state):
		channel = self._check_dio_channel_input(channel)
		self.d.getFeedback(u6.BitStateWrite(channel, state))

	def set_dio_pulse(self, channel, rising=True, duration=1):
		"""sets pulse on on given channel"""

		### not tested yet ###
		
		self.set_dio_state(channel, int(rising))
		time.sleep(duration)
		self.set_dio_state(channel, int(not rising))

	def get_dio_dir(self,channel):
		channel = self._check_dio_channel_input(channel)
		rtn = self.d.getFeedback(u6.BitDirRead(channel))
		return rtn[0]

	def set_dio_dir(self, channel, state):
		channel = self._check_dio_channel_input(channel)
		self.d.getFeedback(u6.BitDirWrite(channel, state))


## handle input
	def _check_dio_channel_input(self, channel):
		""" checks if given channel name is a valid U6 channel name"""
		if channel in self.dio_dct.keys():
			channel = self.dio_dct[channel]
		if channel not in self.dio_dct.values():
			raise DAQUnitError('channel is not a known U6 channel name')
		return channel




# U6 channel name mapping
DIO_DCT = {
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

AI_DCT = {
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

AO_DCT = {
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
	'pressure':		{'ResolutionIndex':0, 'GainIndex':0, 'SettlingFactor':0, 'Differential':False},
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



