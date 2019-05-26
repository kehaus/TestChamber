""" """


from src.util.worker_thread import WorkerTaskBase



class CC(object):

	def __init__(self):
		super().__init__()

		self.a = 1
		self.b = 2

	def __getattr__(self, attr):
		print('getattr:', attr)

	def __getattribute__(self, attr):
		super().__getattribute__(attr)
		print('getattribute:', attr)
		return super(CC, self).__getattribute__(attr)

	def func1(self, a):
		return a**2



class AA(object):
	""" """

	def func1(self, a):
		return a**3

class BB(object):
	""" """
	def __init__(self, bb):
		print('bb :', bb)
		self.bb = bb

	def printb(self, a, c=3):
		print('***bb*** ', self.bb)
		print('**a*** ', a)
		print('***c*** ', c)



class Wrapper(object):
	""" """

	def __init__(self, obj, q):
		self._wrapped_obj = obj
		self.q = q

	def __getattr__(self, attr):
		self.attr = attr
		return self._get_args_kwargs
#		return getattr(self._wrapped_obj, attr)

	def _get_args_kwargs(self, *args, **kwargs):
		self.args = args
		self.kwargs = kwargs

		wt = WorkerTaskBase(self._wrapped_obj, self.attr)
		wt.load_args_kwargs(*args, **kwargs)

		self.q.put(wt)




