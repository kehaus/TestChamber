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





PIN_CONFIG = {	# schematics of external devices connectde to U6 pins
	5:			'FIO0',
	'E':		'FIO1',
	6:			'FIO2',
	'F':		'FIO3',
	7:			'FIO4',
	'H':		'FIO5',
	'X':		'FIO6',
	'Y':		'FIO7',
	'Z':		'VS',
	'L':		'AI1',
	'R':		'GND',
	9:			'EIO0',
	'K':		'EIO1',
	'PKR251_2':	'AI0',
	'PKR251_3':	'GND'
}

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

AI_SETTINGS = {	# contains AI channel settings
	'AI1':		{'ResolutionIndex':0, 'GainIndex':0, 'SettlingFactor':0, 'Differential':False},
}

DIO_SETTINGS = {
	'FIO0':		'di',
	'FIO1':		'di',
	'FIO2':		'di',
	'FIO3':		'di',
	'FIO4':		'di',
	'FIO5':		'di',
	'FIO6':		'di',
	'FIO7':		'di',
	'EIO0':		'do',
	'EIO1':		'do',
}
DIO_DIRECTION = {
	'di':	0,
	'do':	1
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
		"""checks if pin_config variable is of type dictionary"""
		if type(pin_config) != dict:
			raise DAQUnitError('pin_config variable must be of type dict')
		return



# ==============================================================================
# DAQUnit class
# ==============================================================================
class AINReader(object):
	""" """

	AIN24AR_DEFAULT_SETTINGS = {
		'ResolutionIndex':	0,
		'GainIndex':		0,
		'SettlingFactor':	0,
		'Differential':		False
	}

	def __init__(self, **kwargs):
		""" """
		self.settings = AINReader.AIN24AR_DEFAULT_SETTINGS
		self.settings.update(kwargs)
		pass




class DAQUnitBase(DAQUnitExceptionHandling):
	""" """

	def __init__(self, pin_config=None, pin_settings={}, **kwargs):
		""" """
#		self.check_pin_config_type(pin_config)
		self.setup_daq()

		if pin_config is None: 
			pin_config = PIN_CONFIG.copy()
		self.pc = pin_config
		self.ps = pin_settings

		self._init_ai_channel()
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

	def _init_ai_channel(self):
		""" """
		self.ai_lst = self._find_ai_channels(self.pc)
		for ai_name in self.ai_lst:
			if ai_name in AI_SETTINGS.keys():
				setattr(self, ai_name.lower(), 
					AINReader(**AI_SETTINGS.get(ai_name))
				)
			else:
				setattr(self, ai_name.lower(),	AINReader())
		return

	def _init_dio_channel(self):
		"""sets DIO channels to Input or output as specifed in the ''DIO_SETTINGS''
		dictionary

		"""
		self.dio_lst = self._find_dio_channels(self.pc)
		for dio_name in self.dio_lst:
				self.set_dio_dir(
					dio_name, 
					DIO_DIRECTION[DIO_SETTINGS[dio_name]]
				)
		return




	def _find_ai_channels(self, pin_config):
		"""returns list of AI channels specified in pin_config dictionary"""
		ai_lst = [
			x for x in list(pin_config.values()) if x[:2] == 'AI'
		]
		return ai_lst


	def _find_dio_channels(self, pin_config):
		"""returns list of DIO channels specified in pin_config dictionary"""
		dio_lst = [
			x for x in list(pin_config.values()) if x[1:3] == 'IO'
		]
		return dio_lst


#	def get_pressure(self):
#		""" """
#		positiveChannel = ai_dct[self.pc['pressure']]
#		kwargs = self.ps
#		return self.d.getAIN(positivechannel, **kwargs)

	def get_dio_state(self, channel):
		"""return DIO state. 1=High, 0=Low"""
		channel = self._check_dio_channel_input(channel)
		cmd = u6.BitStateRead(channel)
		reading = self.d.getFeedback(cmd)
		return reading[0]

	def set_dio_state(self,channel, state):
		"""sets DIO state. 1=High, 0=Low"""
		channel = self._check_dio_channel_input(channel)
		cmd = u6.BitStateWrite(channel, state)
		self.d.getFeedback(cmd)

	def set_dio_pulse(self, channel, rising=True, duration=1):
		"""sets pulse on on given channel"""

		### not tested yet ###

		self.set_dio_state(channel, int(rising))
		time.sleep(duration)
		self.set_dio_state(channel, int(not rising))

	def get_dio_dir(self,channel):
		"""returns DIO direction. 0=Input, 1=Output"""
		channel = self._check_dio_channel_input(channel)
		cmd = u6.BitDirRead(channel)
		reading = self.d.getFeedback(cmd)
		return reading[0]

	def set_dio_dir(self, channel, state):
		"""sets DIO direction. 0=Input, 1=Output"""
		channel = self._check_dio_channel_input(channel)
		cmd = u6.BitDirWrite(channel, state)
		self.d.getFeedback(cmd)

	def get_ai_value(self, channel, **kwargs):
		""" """
		channel = self._check_ai_channel_input(channel)

		# retrieve ai channel object from channel number
		ai_name = list(AI_DCT.keys())[list(AI_DCT.values()).index(channel)]
		ai_obj = getattr(self, ai_name.lower())

		# measure voltage
		ai_obj.settings.update(kwargs)
		cmd = u6.AIN24AR(channel, **ai_obj.settings)
		reading = self.d.getFeedback(cmd)
		volt = self.d.binaryToCalibratedAnalogVoltage(
			ai_obj.settings['GainIndex'], 
			reading[0]['AIN']
		)
		return volt



## handle input
	def _check_dio_channel_input(self, channel):
		"""checks if given channel name is a valid U6 DIO channel name"""
		if channel in DIO_DCT.keys():
			channel = DIO_DCT[channel]
		if channel not in DIO_DCT.values():
			raise DAQUnitError('channel is not a known U6 channel name.')
		return channel

	def _check_ai_channel_input(self, channel):
		"""checks if given channel is a valid U6 AIN channel name"""
		if channel in AI_DCT.keys():
			channel = AI_DCT[channel]
		if channel not in AI_DCT.values():
			raise DAQUnitError('channel is not a known U6 channel name.')
		return channel



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



