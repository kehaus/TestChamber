"""
Contains various general utility classes with are used by various modules in
the TestChamber repository 


date:	05/17/2019
"""
__version__ = "1.0.0"
__author__		= "kha"



#======================================
# TimeFormatter
#======================================
class TimeFormatterException(Exception):
	pass

class TimeFormatter(object):
	"""class to provide get_time_stamp function

	is used as an attempt to homogenize time stamp format among classes 
	in repository

	Example:
		>>> tf = TimeFormatter()
		>>> tf.get_time_stamp(format_type=None)
		"%Y-%m-%d_%H-%M-%S"
	or 
		>>> TimeFormatter.get_time_stamp()


	"""

	TIME_FORMAT_TYPES = {
		1:		"%Y-%m-%d_%H-%M-%S",
	}

	DEFAULT_TIME_FORMAT = 1

	@staticmethod
	def get_time_stamp(fmt_type=None):
		"""returns current time in specified time format"""
		from time import strftime, gmtime
		
		if fmt_type == None:
			fmt_type = TimeFormatter.DEFAULT_TIME_FORMAT
		if fmt_type not in TimeFormatter.TIME_FORMAT_TYPES.keys():
			raise TimeFormatterException('invalid fmt_type')

		time_stamp = strftime(
			TimeFormatter.TIME_FORMAT_TYPES[fmt_type],
			gmtime()
		)

		return time_stamp

	def get_time_stamp_skeleton(t_stamp):
		"""returns structure of given time_stamp

		**obsolet**

		Example:
			>>> t_stamp = '2019-05-18_06-44-14'
			>>> TimeFormatter.get_time_stamp_skeleton(t_stamp)
			'--_--'

		
		"""
		return ''.join([c for c in t_stamp if not c.isdigit()])

	def get_time_fmt_skeleton_(fmt_type):
		"""returns structure of given format_type

		**obsolet**

		Example:
			>>> fmt_type = "%Y-%m-%d_%H-%M-%S"
			>>> TimeFormatter.get_fmt_skeleton(fmt_type)
			'--_--'
		
		
		"""
		return ''.join([c for c in fmt_type if not c.isalpha() and c != '%'])

	def get_fmt_skeleton(time_str):
		"""returns structure of given t_str. t_str can be a t_stamp or a t_fmt


		Example:
			>>> t_fmt = "%Y-%m-%d_%H-%M-%S"
			>>> TimeFormatter.get_fmt_skeleton(t_fmt)
			'--_--'

			or

			>>> t_stamp = '2019-05-18_06-44-14'
			>>> TimeFormatter.get_fmt_skeleton(t_stamp)
			'--_--'


		 """
		fmt_skltn = ''.join([
			c for c in time_str if 
			not c.isalpha() and 
			not c.isdigit() and 
			not c == '%'
		])
		return fmt_skltn


	def find_format_type(t_stamp):
		"""detects format time of given t_stamp by comparing to 
		TIME_FORMAT_TYPES entries

		"""
		t_skltn = TimeFormatter.get_fmt_skeleton(t_stamp)

		fmt_type = None
		for key, val in TimeFormatter.TIME_FORMAT_TYPES.items():
			fmt_skltn = TimeFormatter.get_fmt_skeleton(val)
			if t_skltn == fmt_skltn:
				fmt_type = key
		if fmt_type == None:
			raise TimeFormatterException('t_stamp format type not known')
		return fmt_type


	@staticmethod
	def get_time_difference(t_stamp):
		"""returns time duration from given t_stampe to now in seconds"""
		from datetime import datetime

		fmt_type = TimeFormatter.find_format_type(t_stamp)
		t_now = TimeFormatter.get_time_stamp(fmt_type=fmt_type)
		fmt = TimeFormatter.TIME_FORMAT_TYPES[fmt_type]

		dt = datetime.strptime(t_now, fmt) - datetime.strptime(t_stamp, fmt)
		return dt.total_seconds()





#======================================
# CSVHandler
#======================================
class CSVHandlerException(Exception):
	pass

class CSVHandler(object):
	"""class provides functions to save data to csv-files 

	Class can be used as parent class for any class which needs to have
	functionality implemented here.

	Example:
		>>> fn = 'test.txt'
		>>> lst = [1,2,4]
		>>> CSVHandler.save_row(fn, lst)


	 """

	DEFAULT_CSV_OPEN_SETTINGS = {
		'mode':			'a',
		'encoding':		'utf-8',
		'newline':		'',
	}

	@staticmethod
	def save_row(fn, lst, **kwargs):
		import csv

		save_settings = CSVHandler.DEFAULT_CSV_OPEN_SETTINGS.copy()
		save_settings.update(kwargs)

		with open(fn, **save_settings) as f:
			writer = csv.writer(f)
			writer.writerow(lst)
		return




#======================================
# JSONHandler
#======================================
class JSONHandlerException(Exception):
	pass

class JSONHandler():
	""" """

	DEFAULT_JSON_OPEN_SETTINGS = {
		'mode':			'a',
		'encoding':		'utf-8',
		'newline':		'',		
	}

	DEFAULT_JSON_DUMP_SETTINGS = {
		'sort_keys':		True,
		'indent':			4,
	}

	@staticmethod
	def save_json(fn, json_dct, **kwargs):
		""" """
		import json

		if not isinstance(json_dct, dict):
			raise JSONHandlerException('json_dct not valid. Must be of dict')

		save_settings = JSONHandler.DEFAULT_JSON_OPEN_SETTINGS.copy()
		save_settings.update(kwargs)

		with open(fn, **save_settings) as f: 
			json.dump(json_dct, f, **JSONHandler.DEFAULT_JSON_DUMP_SETTINGS)
		return



#======================================
# JSONHandler
#======================================
class DataSetException(Exception):
	""" """

class DataSet(CSVHandler, JSONHandler, TimeFormatter):
	""" """

	DEFAULT_PRM = {
		'time_stamp':	'',
		'fn':			'',
		'axes':		['time', 'variable'],
	}

	DEFAULT_BASENAME = 'dataset'

	def __init__(self, base_name=None):
		""" """
		self.time_stamp = self.get_time_stamp()
		if base_name == None:
			base_name = self.DEFAULT_BASENAME
		self.base_name = base_name
		self.fn = self._generate_fn()

		# populate parameter dictionary
		self.prm = self.DEFAULT_PRM.copy()
		self.prm.update({'fn': self.fn})
		self.prm.update({'time_stamp': self.time_stamp})
		self.prm.update({'base_name': self.base_name})

		# create storage files
		self._generate_json()
		self._generate_csv()


	def _generate_fn(self, base_name=None):
		""" """
		return '_'.join([self.time_stamp, self.base_name])

	def get_json_fn(self):
		return '.'.join([self.fn, '.json'])

	def get_csv_fn(self):
		return '.'.join([self.fn, '.csv'])

	def _generate_json(self):
		fn = self.get_json_fn()
		self.save_json(fn, self.prm)

	def _generate_csv(self):
		fn = self.get_csv_fn()
		self.save_row(fn, self.prm['axes'])

	def save_data_point(self, *vals):
		""" """
		fn = self.get_csv_fn()
		dt = self.get_time_difference(self.time_stamp)
		self.save_row(fn, [dt] + list(vals))
		return






