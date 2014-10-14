import os
import subprocess
import yaml
import json

## @todo: mainly missing some log
## @todo: no additional parameters for now, to add
class BaseContainer:
	""" Base container, herited by all container types """

	## Status constants
	UNDEFINED = 0
	RUNNING = 1
	STOPPED = 2

	def __init__(self, path, configuration = None):
		""" load default attributes """

		self.__name = ''
		self.__order = 0
		self.__options = []
		self.__inspect = None
		self.__path = path

		self.init(configuration)
		self.__internal_name = "raiden-" + self.name
		self.__internal_image_name = "raiden-" + self.name + "-image"

	def init(self, configuration):
		""" Init the container object using configuration object """

		self.__name = configuration['name']
		self.__order = configuration['order']
		self.__options = configuration['options']

	# Well ... need some work here
	# But really need something basic for now
	def status(self):
		""" Get container running status """

		DEVNULL = open(os.devnull, 'wb')
		docker_containers = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE)
		if not subprocess.call(['grep', self.__internal_name], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
			DEVNULL.close()
			return self.RUNNING
		docker_containers = subprocess.Popen(['docker', 'ps', '-a'], stdout=subprocess.PIPE)
		if not subprocess.call(['grep', self.__internal_name], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
			DEVNULL.close()
			return self.STOPPED
		DEVNULL.close()
		return self.UNDEFINED

	def build(self):
		""" Build a container from it's defined image """

		print "building container image " + self.__internal_image_name
		DEVNULL = open(os.devnull, 'wb')
		subprocess.call(["docker", "build", "-t", self.__internal_image_name, self.path], stdout=DEVNULL, stderr=DEVNULL)
		DEVNULL.close()


	# same here need some work :)
	def run(self):
		""" Run a container using defined options. Build image if needed. """

		status = self.status()
		if status == self.RUNNING:
			print "container " + self.__internal_name + " already running"

		if status == self.UNDEFINED:
			self.build()
		
		DEVNULL = open(os.devnull, 'wb')
		if status == self.STOPPED:
			print "resuming container " + self.__internal_name
			subprocess.call(['docker', 'start', self.__internal_name], stdout=DEVNULL, stderr=DEVNULL)
		else:
			print "running container " + self.__internal_name
			subprocess.call(['docker', 'run', '-tid', '-p', '80:80', '--name', self.__internal_name, self.__internal_image_name], stdout=DEVNULL, stderr=DEVNULL)
		DEVNULL.close()

		return True

	##
	## Getters and Setters definition
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

	@property
	def path(self):
		return self.__path
