import subprocess

class BaseCommand(object):
	""" Build a docker command from command type and configuration """

	def __init__(self):

		self.params = []
		self.main_command = None
		self.filters = []

	def filter(self, param):
		""" Filter a param, take a param tupple and return the new one """

		if param[0] in self.filters:
			try:
				filter_method = getattr(self, "filter_" + param[0])
				return filter_method(param)
			except AttributeError:
				print "Filter filter_" + param[0] + " not implemented passing"
				pass

			return param

	def addParam(self, param):
		""" Add a parameter to command line from tupple """

		filtered = self.filter(param)
		if filtered != None and isinstance(filtered, list):
			self.params.extend(filtered)
		elif filtered != None:
			self.params.append(filtered)

		return self

	def addParams(self, params):
		""" Add parameters to command line from an array of tupple """

		for param, value in params.iteritems():
			self.addParam([param, value])

		return self

	def execute(self, container):
		""" Execute command """

		if self.main_command == None:
			raise Exception("No command defined")

		print "Executing " + self.main_command

		# DEVNULL = open(os.devnull, 'wb')
		# subprocess.call(self.main_command.split(' ') + self.params stdout=DEVNULL, stderr=DEVNULL)
		# DEVNULL.close()

		return True