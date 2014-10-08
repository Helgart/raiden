import yaml

class BaseContainer:
	""" Base container, herited by all container types """

	def __init__(self, configuration_file = None):
		""" load default attributes """

		if configuration_file is None:
			return;
		stream = open(configuration_file, 'r')
		configuration = yaml.load(stream)
		self.init(configuration)

	def init(self, configuration):
		""" Init the container object using configuration object """

		self.__name = configuration['name']
		self.__order = configuration['order']
		self.__options = configuration['options']

	def build(self):
		""" Build a container from it's defined image """

		print "building container image"

	def run(self):
		""" Run a container using defined options """

		print "running container" 

	##
	## Getters and setters definition
	##

	@property
	def name(self):
	    return self.__name

	@property
	def order(self):
	    return self.__order

	@property
	def options(self):
	    return self.__options