import os
import subprocess
import json

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

		self.__name = ''
		self.__order = 0
		self.__options = []
		self.__inspect = None
		self.__path = path
		self.__status = None

		self.init(configuration)
		self.__internal_name = "raiden-" + self.name
		self.__internal_image_name = "raiden-" + self.name + "-image"

	def init(self, configuration):
		""" Init the container object using configuration object """

		self.__name = configuration['name']
		self.__order = configuration['order']
		self.__options = configuration['options']

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

		print "Inspecting container"
		DEVNULL = open(os.devnull, 'wb')

		## We need to get container state
		## If non 0 return status, container doesn't exists
		try:
			inspect = subprocess.check_output(['docker', 'inspect', self.internal_name], stderr=DEVNULL)
			container_exists = True
			inspect = json.loads(inspect)
		except subprocess.CalledProcessError:
			container_exists = False
			pass

		## No container, so we need to check if we need to build his image or not
		if not container_exists:
			try:
				subprocess.check_call(['docker', 'inspect', self.internal_image_name], stdout=DEVNULL, stderr=DEVNULL)
				self.__status = self.STATUS_BUILD
			except subprocess.CalledProcessError:
				self.__status = self.STATUS_UNKNOWN
				pass

		## We have a container, is it running ? or just stopped ?
		else:
			self.__status = self.STATUS_RUNNING if inspect[0]['State']['Running'] else self.STATUS_STOPPED

		DEVNULL.close()

	##
	## Getters and Setters definition
	##

	@property
	def name(self):
		return self.__name

	@property
	def internal_name(self):
		return self.__internal_name

	@property
	def internal_image_name(self):
		return self.__internal_image_name

	@property
	def order(self):
		return self.__order

	@property
	def options(self):
		return self.__options

	@property
	def path(self):
		return self.__path

	@property
	def status(self):
		if self.__status == None:
			self.refresh_status()
		return self.__status
	
