""" 
Class object definition of RS880Varian gauge controller

Date: 05/04/2019

"""
__author__ = "kha"
__version__ = "0.0.1"


import time




PIN_CONFIG = {
	'mant_lsd_1':			1,
	'mant_lsd_2':			2,
	'mant_lsd_4':			3,
	'mant_lsd_8':			4,
	'exp_lsd_1':			5,
	'exp_lsd_4':			6,
	'exp_msd':				7,
	'disp_update_pulse':	8,
	'filament_on_pulse':	9,
	'TC2_SP_NC':			12,
	'TC2_SP_NO':			13,
	'TC2_SP_common':		14,
#
	'mant_msd_1':			'A',
	'mant_msd_2':			'B',
	'mant_msd_4':			'C',
	'mant_msd_8':			'D',
	'exp_lsd_2':			'E',
	'exp_lsd_8':			'F',
	'exp_sign':				'H',
	'degas_on_off':			'J',
	'filament_off_pulse':	'K',
	'record_output_ion':	'L',
	'digital_GND':			'M',
	'record_output_TC2':	'N',
	'record_output_TC1':	'P',
	'analog_GND':			'R',
	'ion_SP2_common':		'T',
	'ion_SP2_NO':			'U',
	'ion_SP2_NC':			'V',
	'fil_status_NO':		'X',
	'fil_status_NC':		'Y',
	'fil_status_common':	'Z'
}


# ==
#
# ==

class RS880VarianError(Exception):
	""" """
	pass


class RS880Varian(object):
	""" """

	def __init__(self, dd, *args, **kwargs):
		""" """
		super().__init__(*args, **kwargs)
		self.dd = dd
		self.pin_config = PIN_CONFIG
		pass

	def get_exp(self):
		""" """

		bit1 = self.dd.get_dio_state(self.get_pin_name('exp_lsd_1'))
		bit2 = self.dd.get_dio_state(self.get_pin_name('exp_lsd_2'))
		bit4 = self.dd.get_dio_state(self.get_pin_name('exp_lsd_4'))
		bit8 = self.dd.get_dio_state(self.get_pin_name('exp_lsd_8'))
		bit_msd = self.dd.get_dio_state(self.get_pin_name('exp_msd'))
		bit_sign = self.dd.get_dio_state(self.get_pin_name('exp_sign'))

		return [bit_sign, bit_msd, bit8, bit4, bit2, bit1]

	def calc_exp(self, bit_lst):
		""" """

		# gives the wrong values ... maybe invert individual bits?

		s = '0b'+''.join(['1' if x else '0' for x in bit_lst[1:]])
		return (-1)**bit_lst[0] * int(s, 2)


	def get_pin_name(self, rs880_pin_name):
		"""converts rs880Varian pin convenction to U6 pin convention"""
		self._check_pin_name(rs880_pin_name)
		return self.dd.pc[self.pin_config[rs880_pin_name]]

	def _check_pin_name(self, pin_name):
		"""checks if pin name is in self.pin_config"""
		if pin_name not in self.pin_config.keys():
			raise RS880VarianError('pin_name not known. Not part of pin_config')
		return

	def set_filament_on(self):
		""" """

		### not tested yet ###

		self.dd.set_dio_pulse(
			self.get_pin_name('filament_on_pulse'), 
			rising=False, duration=0.5
		)

	def set_filament_off(self):
		""" """

		### not tested yet ###

		self.dd.set_dio_pulse(
			self.get_pin_name('filament_off_pulse'), 
			rising=False, duration=0.5
		)

	def get_filament_status(self):
		"""

		The instrument has an internal relay associated with the filament. When
		the filament is ON, the realy is energized, and the pins Z and X (N.O.) 
		on the accessory output conector form a short circuit. When the tube 
		filament is OFF, the relay is de-energized and pins Z and Y (N.C.) are 
		connected.

		**function only works properly when 5V is connected to RS880Varian 
		Z-pin**


		"""
		n_o = self.dd.get_dio_status(self.get_pin_name('fil_status_NO'))
		n_c = self.dd.get_dio_status(self.get_pin_name('fil_status_NC'))

		if n_o == n_c:
			raise RS880VarianError(
				'Read back from filament status channels X (N.O.) and Y (N.C.) ' +
				'are inconsistent!'
			)



		return n_o

# =====================================
#
# =====================================