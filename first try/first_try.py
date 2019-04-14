

import u6
import math

d = u6.U6()
d.configU6()


channel 			= 0
resolutionIndex 	= 1
gainIndex 			= 0
settlingFactor 		= 0
differential 		= False

cmd 				= u6.AIN24AR(channel, resolutionIndex, gainIndex, settlingFactor, differential)

reading = d.getFeedback(cmd)
volt = d.binaryToCalibratedAnalogVoltage(gainIndex, reading[0]['AIN'])





d.close()




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




class PKR251(U6Reader):
	""" """

	d = {
		'mbar':	11.33,
		'torr': 11.46,
		'Pa':	9.333,
		'kPa':	12.33	
	}

	def __init__(self, d, channel=0, **kwargs):
		""" """
		super().__init__(d, channel, **kwargs)
		self.p_unit = 'mbar'
		pass

	def get_pressure(self, p_unit=None):
		if p_unit == None: p_unit = self.p_unit
		volt = self.get_reading()
		return PKR251.voltage_to_pressure(volt, p_unit)


	@staticmethod
	def voltage_to_pressure(u, p_unit='mbar'):
		""" """
		p = PKR251.conversion_formula(u, PKR251.d[p_unit])
		return p

	@staticmethod
	def conversion_formula(u,d):
		"""conversion formula from Pfeiffer PKR251 manual"""
		return 10**(1.667*u-d)




