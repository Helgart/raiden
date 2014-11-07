import subprocess
import os

from launcher.utilities.printer import Printer

class BaseCommand(object):
	""" Build a docker command from command type and configuration """

	RETURN_SUCCESS = 0
	RETURN_WONT_DO = -1

	def __init__(self):

		self.params = []
		self.main_command = None
		self.filters = []
		self.trigger = []

		self.__printer = Printer()

	def filter(self, param, container = None):
		""" Filter a param, take a param tupple and return the new one """

		if param[0] in self.filters:
			try:
				filter_method = getattr(self, "filter_" + param[0])
				self.__printer.debug("Command", "Executing filter " + param[0])
				return filter_method(param, container)
			except AttributeError:
				self.__printer.warning("Command", "Filter " + param[0] + " not implemented passing")
				pass

			return param

	def addParam(self, param, container = None):
		""" Add a parameter to command line from tupple """

		filtered = self.filter(param, container)
		self.__printer.debug("Command", "Adding parameter : " + str(filtered))
		if filtered != None and isinstance(filtered, list):
			self.params.extend(filtered)
		elif filtered != None:
			self.params.append(filtered)

		return self

	def addParams(self, params, container = None):
		""" Add parameters to command line from an array of tupple """

		for param, value in params.iteritems():
			self.addParam([param, value], container)

		return self

	def manage_output(self, returncode, stdout, stderr):
		""" Manage command output """

		if stdout:
			self.__printer.debug("Command output", stdout)
		if stderr and returncode == 0:
			self.__printer.debug("Command output", stderr)
		elif stderr and returncode:
			self.__printer.error("Command output", stderr)

	def execute(self, container):
		""" Execute command """

		if self.main_command == None:
			raise Exception("No command defined")

		self.__printer.debug("Command", "Executing '" + self.main_command + str(self.params).strip('[]') + "'")
		proc = subprocess.Popen(self.main_command.split(' ') + self.params, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = proc.communicate()

		return self.manage_output(proc.returncode, stdout, stderr)