import datetime

from singleton import Singleton
from color import Color

class Printer:
	""" Printer utility, can display depending on 4 mods : debug, info, warning and error """

	__metaclass__ = Singleton

	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3

	def __init__(self):
		self.level = self.INFO

	def debug(self, origin, message):
		""" print a debug message """

		if self.level > self.DEBUG:
			return

		print '[DEBUG][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message

	def info(self, origin, message):
		""" print an info message """

		if self.level > self.INFO:
			return

		print Color.INFO + '[INFOS][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC

	def warning(self, origin, message):
		""" print a warning message """

		if self.level > self.WARNING:
			return

		print Color.WARNING + '[WARNING][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC

	def error(self, origin, message):
		""" print an error message """

		if self.level > self.ERROR:
			return

		print Color.FAIL + '[ERROR][' + str(datetime.datetime.now()) + '][' + origin + '] ' + message + Color.ENDC