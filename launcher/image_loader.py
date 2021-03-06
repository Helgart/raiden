import os
import yaml

from utilities.printer import Printer

from container.base_container import BaseContainer
from container.application import Application
from container.platform import Platform
from container.layer import Layer
from container.data import Data

class ImageLoader:
	""" Instanciate a container class from a configuration file """

	def load(self, path):
		""" Instanciate a container class from a configuration file """

		printer = Printer()

		configuration_file = path + "/raiden.yml"

		printer.debug("Loader", "Loading file " + configuration_file)

		## In next version values will be generated and saved in a file
		## But for now we must have a configuration file with at least a name
		if configuration_file is None:
			raise Exception("Configuration file is mandatory")
		if not os.path.isfile(configuration_file):
			raise Exception("Configuration file " + configuration_file + " is invalid")

		## Opening configuration file
		stream = open(configuration_file, 'r')
		configuration = yaml.load(stream)

		## Some dynamic import will be added here in future
		## But right now, no use for it
		if configuration['type'] == "application":
			printer.debug("Loader", "Container type: Application")
			image = Application(path, configuration)
		elif configuration['type'] == "platform":
			printer.debug("Loader", "Container type: Platform")
			image = Platform(path, configuration)
		elif configuration['type'] == "layer":
			printer.debug("Loader", "Container type: Layer")
			image = Layer(path, configuration)
		elif configuration['type'] == "data":
			printer.debug("Loader", "Container type: Data")
			image = Data(path, configuration)
		else:
			printer.debug("Loader", "Unknown container type")
			image = BaseContainer(path, configuration)

		## Adding environements
		if configuration.has_key('environements'):
			for env_name, env_values in configuration['environements'].items():
				image.addEnv(env_name, env_values)

		return image