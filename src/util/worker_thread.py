""" 


"""


import threading
import queue
import time
import inspect


class WorkerException(Exception):
	""" """
	pass


class WorkerThread(threading.Thread):

	def __init__(self, q):
		super(WorkerThread, self).__init__()
		self.q = q
		self._stop = True

		self.continous_items = [
			(func2, [1,2], None),
			(func2, [3,4], None)
		]
		self._add_continous_items_to_queue()




	def run(self):

		self._stop = False
		while not self._stop:
			if not self.q.empty():	
				self.process_item()
				time.sleep(1)

	def stop(self):
		self._stop = True

	def process_item(self):
		item = self.q.get()
		if item in self.continous_items: self.q.put(item)
		func, args, kwargs = item

		if args == None:
			args = []
		if type(args) != list:
			raise WorkerExcpetion("args needs to be of type list.")

		if kwargs == None:
			kwargs = {}
		if type(kwargs) != dict:
			raise WorkerException("kwargs needs to be of type dict.")

		val = func(*args, **kwargs)
		print(val)


	def _add_continous_items_to_queue(self):
		for item in self.continous_items:
			self.q.put(item)
		return



def func1():
	print('func1')
	return

def func2(x,y, z=8):
	print('func2')
	print('x: ', x, 'y: ', y, 'z: ', z)
	return

def func3(v=33, w=55, z=9):
	print('func3')
	print('v: ', v, 'w: ', w, 'z: ',z)
	return




