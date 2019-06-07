"""
DAQ unit control class



TODO:
1. write mocking class for u6. Necessary to develop code without being dependent 
on hardware connected. need to mock

* open in U6 and DEvice
* _writeRead in U6
* write() in U6
* read() in U6


Examples
for debugging U6 communication:

	>>> d = u6.U6()
	>>> d.configU6()
	>>> channel_nr = 4
	>>> d.getAIN(channl_nr)

"""
__version__ = "0.0.1"
__author__ = "kha"


import u6
import time
from thermocouples_reference import thermocouples





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
	'L':		'AI121',
	'R':		'GND',
	9:			'EIO0',
	'K':		'EIO1',
	'PKR251_2':	'AI120',
	'PKR251_3':	'GND',
	'SM7022_1':	'GND',
	'SM7022_2':	'AI2',
	'SM7022_3':	'AO1',
	'SM7022_10':	'AI3',
	'ES030_1':	'GND',
	'ES030_2':	'AI0',
	'ES030_3':	'AO0',
	'ES030_10':	'AI1',
	'HSTC_CH':	'AI12',
	'HSTC_AL':	'AI13',
	'TC1_CH':	'AI48',
	'TC1_AL':	'AI56',
	'TC2_CH':	'AI49',
	'TC2_AL':	'AI57',
	'TC3_CH':	'AI50',
	'TC3_AL':	'AI58',
	'TC4_CH':	'AI51',
	'TC4_AL':	'AI59',
	'TC5_CH':	'AI52',
	'TC5_AL':	'AI60',
	'TC6_CH':	'AI53',
	'TC6_AL':	'AI61'
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
# Block 1 - P
	'AI48':		48,
	'AI49':		49,
	'AI50':		50,
	'AI51':		51,
	'AI52':		52,
	'AI53':		53,
	'AI54':		54,
	'AI55':		55,
# Block 1 - N
	'AI56':		56,
	'AI57':		57,
	'AI58':		58,
	'AI59':		59,
	'AI60':		60,
	'AI61':		61,
	'AI62':		62,
	'AI63':		63,
# Block 2 - P
	'AI64':		64,
	'AI65':		65,
	'AI66':		66,
	'AI67':		67,
	'AI68':		68,
	'AI69':		69,
	'AI70':		70,
	'AI71':		71,
# Block 2 - N
	'AI72':		72,
	'AI73':		73,
	'AI74':		74,
	'AI75':		75,
	'AI76':		76,
	'AI77':		77,
	'AI78':		78,
	'AI79':		79,
# Block 3 - P
	'AI80':		80,
	'AI81':		81,
	'AI82':		82,
	'AI83':		83,
	'AI84':		84,
	'AI85':		85,
	'AI86':		86,
	'AI87':		87,
# Block 3 - N
	'AI88':		88,
	'AI89':		89,
	'AI90':		90,
	'AI91':		91,
	'AI92':		92,
	'AI93':		93,
	'AI94':		94,
	'AI95':		95,
# Block 4 - P
	'AI96':		96,
	'AI97':		97,
	'AI98':		98,
	'AI99':		99,
	'AI100':	100,
	'AI101':	101,
	'AI102':	102,
	'AI103':	103,
# Block 4 - N
	'AI104':	104,
	'AI105':	105,
	'AI106':	106,
	'AI107':	107,
	'AI108':	108,
	'AI109':	109,
	'AI110':	110,
	'AI111':	111,
# Block 5 - P
	'AI112':	112,
	'AI113':	113,
	'AI114':	114,
	'AI115':	115,
	'AI116':	116,
	'AI117':	117,
	'AI118':	118,
	'AI119':	119,
# Block 5 - N
	'AI120':	120,
	'AI121':	121,
	'AI122':	122,
	'AI123':	123,
	'AI124':	124,
	'AI125':	125,
	'AI126':	126,
	'AI127':	127
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

class BaseChannel(object):
	"""Base class for a Labjack U6 Analog input or output channel"""

	def __init__(self, dd, pin_config=None):
		""" """
		self.dd = dd
		if pin_config == None:
			pin_config = PIN_CONFIG
		self.pin_config = pin_config
		return 

	def get_u6_pin_name(self, dev_pin_name):
		""" """
		if type(dev_pin_name) is list:
			return [self.get_u6_pin_name(x) for x in dev_pin_name]
		self._check_pin_name(dev_pin_name)
		u6_pin_name = self.dd.pc[self.pin_config[dev_pin_name]]
		return u6_pin_name		

	def _check_pin_name(self, pin_name):
		"""checks if pin name is in self.pin_config"""
		if pin_name not in self.pin_config.keys():
			raise DAQUnitError('pin_name not known. Not part of pin_config')
		return


class AI_channel(BaseChannel):
	"""represents a LabJack U6 analog input channel

	This class allows do directly read out AIN channels from the U6. It 
	furthermore takes care of mapping the device pin_name to the 
	corresponding U6 pin_name representation

	"""

	def get_ai_value(self, dev_pin_name):
		""" """
		val = self.dd.get_ai_value(
			self.get_u6_pin_name(dev_pin_name))
		return val

class AO_channel(BaseChannel):
	"""represents a LabJack U6 analog output channel

	This class allows do directly read out AIN channels from the U6. It 
	furthermore takes care of mapping the device pin_name to the 
	corresponding U6 pin_name representation

	"""

	def set_ao(self, dev_pin_name, value):
		u6_pin_name = self.get_u6_pin_name(dev_pin_name)
		self.dd.set_ao(u6_pin_name, value)
	

class DIO_channel(BaseChannel):
	""" """
	pass



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
		self.settings = AINReader.AIN24AR_DEFAULT_SETTINGS.copy()
		self.settings.update(kwargs)
		pass


class DAQUnitBase(DAQUnitExceptionHandling):
	""" """

	DAC_BIT_MAX		= 2**16-1
	DAC_VOLT_MAX	= 10

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

	def get_ai_value(self, channel, verbose=False, **kwargs):
		""" """
		channel = self._check_ai_channel_input(channel)

		# retrieve ai channel object from channel number
		ai_name = list(AI_DCT.keys())[list(AI_DCT.values()).index(channel)]
		ai_obj = getattr(self, ai_name.lower())

		# measure voltage
		ai_obj.settings.update(kwargs)
		cmd = u6.AIN24AR(channel, **ai_obj.settings)
		if verbose: 
			print('cmd: ', cmd)
		reading = self.d.getFeedback(cmd)
		volt = self.d.binaryToCalibratedAnalogVoltage(
			ai_obj.settings['GainIndex'], 
			reading[0]['AIN']
		)
		return volt

	def set_ao(self, channel, volt, **kwargs):
		""" """
		channel = self._check_ao_channel_input(channel)

		bit = self.d.voltageToDACBits(volt, dacNumber=0, is16Bits = True)
		if channel == AO_DCT['AO0']:
			cmd = u6.DAC0_16(bit)
		elif channel == AO_DCT['AO1']:
			cmd = u6.DAC1_16(bit)
		else:
			raise DAQUnitError('channel is not a valid input. Needs to be 0 or 1.')
		self.d.getFeedback(cmd)

	def get_temperature(self):
		"""returns the ambient temperature sensor value in Kelvin

		With enclosure on, the U6 is typically 3°C higher than ambient. The calibration
		constant have taken this into account and have therefore an offset of -3°C, so 
		the returned calibration readings are nominally the same as ambient with the 
		enclosure installed

		for reference check: 
			https://labjack.com/support/datasheets/u6/hardware-description/ain/internal-temp-sensor


		"""
		return self.d.getTemperature()

	def get_internal_temperature(self):
		"""returns the U6's internal temperature sensor value in Kelvin

		"""
		return self.get_temperature + 3


## handle input
	def _check_dio_channel_input(self, channel):
		"""checks if given channel name is a valid U6 DIO channel name"""
		if channel in DIO_DCT.keys():
			channel = DIO_DCT[channel]
		if channel not in DIO_DCT.values():
			raise DAQUnitError('{} is not a known U6 channel name.'.format(channel))
		return channel

	def _check_ai_channel_input(self, channel):
		"""checks if given channel is a valid U6 AIN channel name"""
		if channel in AI_DCT.keys():
			channel = AI_DCT[channel]
		if channel not in AI_DCT.values():
			raise DAQUnitError('{} is not a known U6 channel name.'.format(channel))
		return channel

	def _check_ao_channel_input(self, channel):
		"""checks if given channel is a valid U6 DAC channel name"""
		if channel in AO_DCT.keys():
			channel = AO_DCT[channel]
		if channel not in AO_DCT.values():
			raise DAQUnitError('{} is not known U6 channel name.'.formant(channel))
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



