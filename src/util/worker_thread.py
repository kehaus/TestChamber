""" 


* use unix time as absolute time measure
* save time data for every device seperately
* save parameter in json and data in csv

Example:

>>> wt = WorkerTask(func1)	#func1 needs to be defined already
>>> q = queue.Queue()
>>> q.put(wt)				# load task into queue
>>> w(q)
>>> w.start()				# start thread

"""


import threading
import queue
import csv
import time
import inspect

from ..util.general_util import DataSet, TimeFormatter, CSVHandler, JSONHandler


class WorkerException(Exception):
	""" """
	pass


class WorkerThread(threading.Thread):
	"""



	Example:
		>>> w = WorkerTask(func1, save=True, continuous=True)
		>>> q = queue.Queue()
		>>> q.put(w)
		>>> ww = WorkerThread(q)
		>>> ww.start()

	To stop:
		>>> ww.stop()

	 """

	SLEEP_TIME = 4

	def __init__(self, q):
		super(WorkerThread, self).__init__()
		self.q = q
		self._stop = True
		self.sleep_time = WorkerThread.SLEEP_TIME


	def run(self):

		self._stop = False
		while not self._stop:
			if not self.q.empty():	
				self.process_task()
			time.sleep(self.sleep_time)

	def stop(self):
		self._stop = True

	def process_task(self):
		task = self.q.get()
		if task.continuous: self.q.put(task)
		task.do_task()



class WorkerTaskException(Exception):
	""" """
	pass


class WorkerTask(DataSet):
	""" """

	COUNT = 0
#	DEFAULT_FILE_HEADER = [
#		'time',
#		'variable'
#	]

	def __init__(self, 
				 func, 
				 args=None, 
				 kwargs=None, 
				 continuous=False, 
				 save=False, 
				 plot=False,
                                 base_name=None):
		super().__init__(base_name=base_name)
		WorkerTask.COUNT += 1
		self.continuous = continuous
		self.save = save
		self.fn_base = 'workertask{:d}'.format(WorkerTask.COUNT)
		self.plot = plot

		self.func = self._check_func(func)
		self.args = self._check_args(args)
		self.kwargs = self._check_kwargs(kwargs)

	def _check_func(self, func):
		if callable(func) != True:
			raise WorkerTaskException('func needs to be callable object')
		return func

	def _check_args(self, args):
		if args == None:
			args = []
		if type(args) != list:
			raise WorkerTaskException('args needs to be of type list')
		return args

	def _check_kwargs(self, kwargs):
		if kwargs == None:
			kwargs = {}
		if type(kwargs) != dict:
			raise WorkerTaskException('kwargs needs to be of type dict')
		return kwargs


#	def _generate_fn(self):
#		""" """
#		time_stamp = self.get_time_stamp()
#		fn = '_'.join([time_stamp,self.fn_base])
#		return fn


#	def _create_data_file(self):
#
#		hd = WorkerTask.DEFAULT_FILE_HEADER.copy()
#
#		self.fn = self._generate_fn()
#		self._save_data_point(hd)
#		return


#	def _save_data_point(self, lst):
#
#		if not hasattr(self, fn):
#			self._create_data_file()
#		self.save_row(self.fn,)
#		return

#	def _save_parameter(self):
#		pass


	def plot_data(self):
		pass

	def do_task(self):

		self.rtn = self.func(*self.args, **self.kwargs)

		if self.save != None:
			self.save_data_point(self.rtn)

		if self.plot != None:
			self.plot_data()
		return


### Dataset class





### Examples usage case

def func1():
	return 'func1'

def func2(x,y, z=8):
	print('func2')
	print('x: ', x, 'y: ', y, 'z: ', z)
	return

def func3(v=33, w=55, z=9):
	print('func3')
	print('v: ', v, 'w: ', w, 'z: ',z)
	return

wt = WorkerTask(func1, continuous=True)
q = queue.Queue()
w = WorkerThread(q)




