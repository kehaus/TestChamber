"""
class definition to read out thermocouple with Labjack U6


date: 05/11/2019
"""

__version__ = "1.0.0"
__author__	= "kha"


from .daqunit import AI_channel, AINReader
from thermocouples_reference import thermocouples

PIN_CONFIG_HS = {
	'chromel':	'HSTC_CH',
	'alumel':	'HSTC_AL'
}

class TC(AI_channel):
	""" """

	AIN_SETTINGS = {
		'ResolutionIndex':	8,
		'GainIndex':		3,
		'Differential':		True
	}

	def __init__(self, *args, **kwargs):
		""" """
		super().__init__(*args, **kwargs)
		if 'pin_config' not in kwargs.keys():
			self.pin_config = PIN_CONFIG_HS.copy()
		self.ain_reader = AINReader(**TC.AIN_SETTINGS)
		self.typeK = thermocouples['K']


	def get_temperature(self):
		""" """
		volt = self.get_ai_value('chromel')	# [uV]
		volt *= 1000						# [mV]
		Tref = self.dd.get_temperature()	# [K]
		Tref -= 273.15						# [C]
		Tmeas = self.typeK.inverse_CmV(volt, Tref=Tref)
		return Tmeas




