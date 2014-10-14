import os
import subprocess
import yaml
import json

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

	def refresh(self):
		""" Refresh container status """

		self.__inspect = None
		DEVNULL = open(os.devnull, 'wb')
		try:
			self.__inspect = json.loads(subprocess.check_output(['docker', 'inspect', self.__internal_name], stderr=DEVNULL))[0]
		except subprocess.CalledProcessError as e:
			if e.returncode == 1:
				pass
			else:
				raise e
		DEVNULL.close()

	# Well ... need some work here
	# A command runner class would be cool !
	# But really need something basic for now
	def status(self):
		""" Get container running status """

		DEVNULL = open(os.devnull, 'wb')
		docker_containers = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE)
		if not subprocess.call(['grep', self.__internal_name], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
			DEVNULL.close()
			return self.RUNNING
		if not subprocess.call(['grep', self.__internal_name, '-a'], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
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
		""" Run a container using defined options """

		print "running container " + self.__internal_name

		return False
		DEVNULL = open(os.devnull, 'wb')
		subprocess.call(['docker', 'run', '-tid', '-p', '80:80', '--name', self.__internal_name, self.__internal_image_name], stdout=DEVNULL, stderr=DEVNULL)
		DEVNULL.close()

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