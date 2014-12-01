import os
import yaml

class Configuration:
	""" Configuration object, all raiden default arguments """

	def __init__(self, arguments):
		
		## Log file configurations
		self.log_path = arguments.log_path
		self.log_level = arguments.log_level
		self.log_name = arguments.log_name if arguments.log_name else "raiden.log"

		## Environement specifications
		self.environement = arguments.env

		## default pool paths
		self.pools = pools = list(set(arguments.pools.split(','))) if arguments.pools else '.'

	def loadFile(self):
		""" Load a YAML configuration file to build configuration """
		