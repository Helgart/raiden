import os
import yaml

class Configuration:
	""" Configuration object, all raiden default arguments """

	def __init__(self):
		
		## Log file configurations
		self.log_path = None
		self.log_level = 1
		self.log_name = "raiden.log"
		self.log_file = None

		## Environement specifications
		self.environement = None

		## default pool paths
		self.pools = pools = '.'

	def load(self, arguments):
		""" Update configurations from dictionary """

		## Log file configurations
		self.log_path = arguments['log_path'] if arguments['log_path'] else self.log_path
		self.log_level = arguments['log_level'] if arguments['log_level'] else self.log_level
		self.log_name = arguments['log_name'] if arguments['log_name'] else self.log_name
		self.log_file = arguments['log_path'] + '/' + self.log_name if arguments['log_path'] else self.log_file

		## Environement specifications
		self.environement = arguments['environement'] if arguments['environement'] else self.environement

		## default pool paths
		self.pools = pools = list(set(arguments['pools'])) if arguments['pools'] else self.pools

	def loadFile(self, configuration_file):
		""" Load a YAML configuration file to build configuration """

		if not os.path.isfile(configuration_file):
			raise Exception("Configuration file " + configuration_file + " is invalid")

		## Opening configuration file
		stream = open(configuration_file, 'r')
		configuration = yaml.load(stream)

		self.load(configuration)