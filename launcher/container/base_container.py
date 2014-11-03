import os
import os.path
import subprocess
import json

from launcher.utilities.printer import Printer

## @todo: mainly missing some log
## @todo: no additional parameters for now, to add
## @todo: no docker command should be run here, need to change that
class BaseContainer(object):
	""" Base container, herited by all container types """

	STATUS_UNKNOWN = 0
	STATUS_RUNNING = 1
	STATUS_STOPPED = 2
	STATUS_BUILD = 3

	def __init__(self, path, configuration = None):
		""" load default attributes """

		self.__printer = Printer()

		self.name = ''
		self.path = path
		self.type = 'base'
		self.dockerfile = ''
		self.environements = {}
		self.currentEnv = None
		self.runnable = True
		
		self.__options = {}
		self.__inspect = None
		self.__status = None
		self.__computedOptions = None

		self.init(configuration, path)
		self.internal_name = "raiden-" + self.type + "-" + self.name
		self.internal_image_name = "raiden-" + self.type + "-" + self.name + "-image"

		self.__printer.debug("Container", "Container " + self.internal_name + " from image " + self.internal_image_name + " loaded")

	def init(self, configuration, path):
		""" Init the container object using configuration object """

		self.name = configuration['name']
		self.type = configuration['type']

		self.dockerfile = os.path.realpath(path + '/' + configuration['dockerfilePrefix']) if 'dockerfilePrefix' in configuration else path
		
		if 'options' in configuration:
			self.__options = configuration['options']

		self.__printer.debug("Container", "Container options")
		self.__printer.debug("Container", "Name : " + self.name)
		self.__printer.debug("Container", "Type : " + self.type)
		self.__printer.debug("Container", "Dockerfile : " + self.dockerfile)
		
		if 'options' in configuration:
			self.__printer.debug("Container", "Options : " + str(map(str, self.__options)))
		else:
			self.__printer.debug("Container", "No options")

	def refresh_status(self):
		"""
			Container inspection to get his status. For now, 3 status :
				- STATUS_UNKNOWN : Container is unknown
				- STATUS_RUNNING : Container is running
				- STATUS_STOPPED : Container is stopped
				- STATUS_BUILD : Container image is build, but container himself has not been run yet
		"""

		## True if container exists
		## Will be used to inspect image if container is missing
		## @todo work on that point ... Implementation is bad
		container_exists = True

		## Will contain container or image inspection
		inspect = None

		self.__printer.debug("Container", "Refreshing container status")
		DEVNULL = open(os.devnull, 'wb')

		## We need to get container state
		## If non 0 return status, container doesn't exists
		self.__printer.debug("Container", "Executing 'docker inspect " + self.internal_name + "'")
		try:
			inspect = subprocess.check_output(['docker', 'inspect', self.internal_name], stderr=DEVNULL)
			self.__printer.debug("Container", "Container existing")
			container_exists = True
			inspect = json.loads(inspect)
		except subprocess.CalledProcessError:
			self.__printer.debug("Container", "Container doesn't exists")
			container_exists = False
			pass

		## No container, so we need to check if we need to build his image or not
		if not container_exists:
			self.__printer.debug("Container", "Executing 'docker inspect " + self.internal_image_name + "'")
			try:
				subprocess.check_call(['docker', 'inspect', self.internal_image_name], stdout=DEVNULL, stderr=DEVNULL)
				self.__printer.debug("Container", "Image already build")
				self.__status = self.STATUS_BUILD
			except subprocess.CalledProcessError:
				self.__printer.debug("Container", "Image not build")
				self.__status = self.STATUS_UNKNOWN
				pass

		## We have a container, is it running ? or just stopped ?
		else:
			self.__status = self.STATUS_RUNNING if inspect[0]['State']['Running'] else self.STATUS_STOPPED

		if self.__status == self.STATUS_RUNNING:
			self.__printer.debug("Container", "Container already running")
		else:
			self.__printer.debug("Container", "Container stopped")

		DEVNULL.close()

	def addEnv(self, name, values):
		""" Load environement running options """

		self.environements[name] = values

	##
	## Getters and Setters definition
	##

	@property
	def options(self):
		if self.currentEnv and self.environements.has_key(self.currentEnv):
			if not self.__computedOptions:
				self.__computedOptions = self.__options.copy()
				self.__computedOptions.update(self.environements[self.currentEnv])
			return self.__computedOptions
		return self.__options

	@property
	def status(self):
		if self.__status == None:
			self.refresh_status()
		self.__printer.debug("Container", "Using status in cache")
		return self.__status
