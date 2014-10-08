import yaml

class BaseContainer:
	""" Base container, herited by all container types """

	def __init__(self, configuration_file = None):
		""" load default attributes """

		if configuration_file is None:
			return;
		stream = open(configuration_file, 'r')
		configuration = yaml.load(stream);
		self.init(configuration)

	def init(self, configuration):
		""" Init the container object using configuration object """

	def build(self):
		""" Build a container from it's defined image """

		print "building container image"

	def run(self):
		""" Run a container using defined options """

		print "running container" 