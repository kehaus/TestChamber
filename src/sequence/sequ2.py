"""
contains short example of how to initialize hardware components with
the python classes from the TestChamber repository.



"""
__version__ = "0.0.2"
__author__ = "kha"


import numpy as np
import queue

from ..daq.daqunit import DAQUnitBase
#from ..daq.sm7022 import ES03010, SM7022, HeaterStage, EffusionCell
from ..daq.sm7022 import ES03010, SM7022, EffusionCell
from ..daq.heaterstage import HeaterStage
from ..daq.pkr251 import PKR251
from ..daq.rs880varian import RS880Varian
from ..daq.tc import TC
from ..daq.iga6 import IGA6

from ..util.worker_thread import WorkerThread, WorkerTask



# ==============
#
# ==============


class HeaterStageReadTask(WorkerTask):
	"""class to read back heaterstage values with WorkerThread

	this class redefines the self.do_task() to read back multiple variables
	and stores them in the measurement file. Three things are important here
		* self.do_task() is redefined
		* self.dummy_func() is defined with the single purpose to give it back to the
		  parent class __init__() function. 
		* DEFAULT_PRM is redefined to adjust adjust the correct axes labels

	 """

	DEFAULT_PRM = {
		'time_stamp':	'',
		'fn':			'',
		'axes':		['time', 'I [A]', 'V [V]', 'T [C]'],
	}

	def __init__(self, hs, *args, **kwargs):
		super().__init__(self.dummy_func, *args, **kwargs)
		self.hs = hs 

	def dummy_func(self):
		""" """
		return

	def do_task(self):

#		self.rtn = self.func(*self.args, **self.kwargs)
#	
		volt = self.hs.get_voltage()
		curr = self.hs.get_current()
		temp = -1  # self.hs.get_temperature()

		if self.save != False:
			self.save_data_point(curr, volt, temp)

		if self.plot != False:
			self.plot_data()
		return
    




class HeaterStageWriteTask(WorkerTask):
	""" """

	def __init__(self, hs, ramp_curve, *args, **kwargs):
		"""

		ramp_curve:	contains information about current ramp-up curve.
		Needs to have specific format


		"""
		super().__init__(hs.set_current, *args, **kwargs)
		self.hs = hs
		self.ramp_curve = ramp_curve

	def _check_ramp_curve_format(self, ramp_curve):
		""" """
		return True

	def _set_start_stop_values(self, ramp_curve_tpl):
		""" """
		self.I_start, self.I_stop, self.dt = ramp_curve_tpl
		self.t_stamp_start = self.get_time_stamp()
		self.set_ramp_mode(self.I_start, self.I_stop, verbose=True)

	# def ramp_current_(self):
	# 	""" 

	# 	**obsolet**

	# 	"""

	# 	if self.reached_I_stop():
	# 		if len(self.ramp_curve) > 0:
	# 			self._set_start_stop_values(self.ramp_curve.pop(0))
	# 		else:
	# 			self.continuous = False
	# 			self.hs.set_current(self.I_stop, verbose=True)
	# 			return
	# 	I_set = self._get_next_current_value()
	# 	if self.ramp_mode == 'ramp_up':
	# 		I_set = self._ramp_up(I_set)
	# 	elif self.ramp_mode == 'ramp_down':
	# 		I_set = self._ramp_down(I_set)
	# 	elif self.ramp_mode == 'constant':
	# 		I_set = self._stay_constant(I_set)
	# 	else:
	# 		raise Exception('ramp_mode value not known')		# TODO: replace by WorkerTaskException later !!
	# 	self.hs.set_current(I_set, verbose=True)
	# 	return

	# def reached_I_stop(self):
	# 	""" 

	# 	**obsolet**

	# 	"""
	# 	if not hasattr(self, 'I_stop'):
	# 		return True
	# 	else:
	# 		I_now = self.hs.get_current()
	# 		return self.compare_current(I_now, self.I_stop, verbose=True)
	

	def reached_t_stop(self):
		"""returns True if time between t_stamp_start and t_now is bigger than dt"""
		if not hasattr(self, 'dt'):
			return True
		else:
			t_now = self.get_time_stamp()
			return self.get_time_difference(self.t_stamp_start) > self.dt

	def compare_current(self, I1, I2, atol=0.1, verbose=False):
		"""returns True if currents I1 and I2 are equal within given tolerance"""
		flag = np.isclose(I1, I2, atol=atol)
		if verbose:
			print('I1: {0:.2f}A, I2: {1:.2f}A, bool: '.format(I1, I2), flag)
		return flag

	def _get_next_current_value(self):
		t_now = self.get_time_difference(self.t_stamp_start)
		I_set = self.I_start
		I_set += (self.I_stop - self.I_start) * t_now / self.dt
		return I_set

	def _ramp_up(self, I_set):
		if I_set < self.I_stop:
			return I_set
		else:
			return self.I_stop

	def _ramp_down(self, I_set):
		if I_set > self.I_stop:
			return I_set
		else:
			return self.I_stop

	def _stay_constant(self, I_set):
		return I_set

	def set_ramp_mode(self, I_start, I_stop, verbose=False):
		if self.compare_current(I_start, I_stop):
			self.ramp_mode = 'constant'
		else:
			if I_start < I_stop:
				self.ramp_mode = 'ramp_up'
			elif I_start > I_stop:
				self.ramp_mode = 'ramp_down'
		if verbose:	print('Ramp mode: {}'.format(self.ramp_mode))
		return


	def ramp_current(self, verbose=False):

		if self.reached_t_stop():
			if len(self.ramp_curve) > 0:
				self._set_start_stop_values(self.ramp_curve.pop(0))
			else:
				self.continuous = False
				self.hs.set_current(self.I_stop, verbose=verbose)
				return
		I_set = self._get_next_current_value()
		if self.ramp_mode == 'ramp_up':
			I_set = self._ramp_up(I_set)
		elif self.ramp_mode == 'ramp_down':
			I_set = self._ramp_down(I_set)
		elif self.ramp_mode == 'constant':
			I_set = self._stay_constant(I_set)
		else:
			raise Exception('ramp_mode value not known')		# TODO: replace by WorkerTaskException later !!
		self.hs.set_current(I_set, verbose=True)
		return

	def do_task(self):

		self.ramp_current()

		if self.save != False:
			print('hs_writer: save data')
			self.save_data_point()

		if self.plot != False:
			self.plot_data()
		return


# ==============
#
# ==============
ramp_curve = [
	(0.0, 1.0, 30),
	(1.0, 1.0, 20),
	(1.0, 0.0, 30)
]

com_genesys = '//dev//ttyUSB1'

dd = DAQUnitBase()
sm = SM7022(dd)
es = ES03010(dd)
pkr = PKR251(dd)
rs = RS880Varian(dd)
hs =HeaterStage(port=com_genesys)
ef = EffusionCell(dd)
###

pkr_wt = WorkerTask(pkr.get_pressure, continuous=True, save=True, base_name='pkr251')
rs_wt = WorkerTask(rs.get_pressure, continuous=True, save=True, base_name='rs880')
hs_read_wt = HeaterStageReadTask(hs, continuous=True, save=True, base_name='hs')
hs_write_wt = HeaterStageWriteTask(hs, ramp_curve, continuous=True, save=False)

ef_read_wt = HeaterStageReadTask(ef, continuous=True, save=True, base_name='ef')
ef_write_wt = HeaterStageWriteTask(ef, ramp_curve, continuous=True, save=False)

q = queue.Queue()

q.put(pkr_wt)
q.put(rs_wt)
q.put(hs_read_wt)
q.put(ef_read_wt)

##com_iga = '//dev//ttyUSB0'
##iga = IGA6(com_iga)
##iga_read_wt = WorkerTask(iga.get_temperature, continuous=True, save=True, base_name='iga6')
##q.put(iga_read_wt)

w = WorkerThread(q)


#iga_write = WorkerTask(iga._query, args=['ms'])
#q.put(iga_write)
#iga_write.rtn


#tc1 = TC(dd, pin_config={'chromel': 'TC1_CH', 'alumel': 'TC1_AL'})
#tc2 = TC(dd, pin_config={'chromel': 'TC2_CH', 'alumel': 'TC2_AL'})
#tc3 = TC(dd, pin_config={'chromel': 'TC3_CH', 'alumel': 'TC3_AL'})
#tc4 = TC(dd, pin_config={'chromel': 'TC4_CH', 'alumel': 'TC4_AL'})


