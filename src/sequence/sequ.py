"""
contains short example of how to initialize hardware components with
the python classes from the TestChamber repository.



"""
__version__ = "0.0.1"
__author__ = "kha"



import queue

from ..daq.daqunit import DAQUnitBase
from ..daq.sm7022 import SM7022
from ..daq.pkr251 import PKR251
from ..daq.rs880varian import RS880Varian

from ..util.worker_thread import WorkerThread, WorkerTask

dd = DAQUnitBase()
sm = SM7022(dd)
pkr = PKR251(dd)
rs = RS880Varian(dd)


###

pkr_wt = WorkerTask(pkr.get_pressure, continuous=True, save=True, base_name='pkr251')
rs_wt = WorkerTask(rs.get_pressure, continuous=True, save=True, base_name='rs880')

q = queue.Queue()

q.put(pkr_wt)
q.put(rs_wt)

w = WorkerThread(q)






class SM7022Task(WorkerTask):
	""" """

	DEFAULT_PRM = {
		'time_stamp':	'',
		'fn':			'',
		'axes':		['time', 'I [A]', 'V [V]'],
	}

	def __init__(self, sm7022, *args, **kwargs):
		super().__init__(self.dummy_func, *args, **kwargs)
		self.sm7022 = sm7022 

	def dummy_func(self):
		""" """
		return

	def do_task(self):

#		self.rtn = self.func(*self.args, **self.kwargs)
#	
		volt = self.sm7022.get_voltage()
		curr = self.sm7022.get_current()

		if self.save != None:
			self.save_data_point(volt, curr)

		if self.plot != None:
			self.plot_data()
		return
    











