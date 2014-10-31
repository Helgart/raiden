import datetime
import os.path

from logging import Logger
from logging import FileHandler
from logging import Formatter
from singleton import Singleton
from color import Color

class Printer:
	"""
		Printer utility, can display depending on 4 mods : debug, info, warning and error
		Will be writen again later with a proper logger implementation
		Bear with it for now !
	"""

	__metaclass__ = Singleton

	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3

	def __init__(self):
		self.level = self.INFO
		self.logger = None

	def setLogger(self, filepath, level):
		""" Define logger """

		if not os.path.isdir(os.path.dirname(filepath)):
			raise Exception("Unknown directory " + os.path.dirname(filepath))

		## Why ? well ... https://docs.python.org/2/library/logging.html#levels
		logLevel = 10 if not level else int(level) * 10
		handler = FileHandler(filepath)
		formatter = Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
		handler.setFormatter(formatter)
		
		self.logger = Logger('main')
		self.logger.addHandler(handler)
		self.logger.setLevel(logLevel)

	def debug(self, origin, message):
		""" print a debug message """

		if self.logger:
			self.logger.debug(message, {'origin' : origin})

		if self.level > self.DEBUG:
			return

		print '[DEBUG][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message

	def info(self, origin, message):
		""" print an info message """

		if self.logger:
			self.logger.info(message, {'origin' : origin})

		if self.level > self.INFO:
			return

		print Color.INFO + '[INFO][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC

	def warning(self, origin, message):
		""" print a warning message """

		if self.logger:
			self.logger.warning(message, {'origin' : origin})

		if self.level > self.WARNING:
			return

		print Color.WARNING + '[WARNING][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC

	def error(self, origin, message):
		""" print an error message """

		if self.logger:
			self.logger.error(message, {'origin' : origin})

		if self.level > self.ERROR:
			return

		print Color.FAIL + '[ERROR][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC