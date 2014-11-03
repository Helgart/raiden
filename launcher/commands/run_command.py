import os
import subprocess

from launcher.utilities.printer import Printer
from base_command import BaseCommand

## @todo In next step, some trigger using container inspect would be nice !
class RunCommand(BaseCommand):
	""" Build a docker command from command type and configuration """

	def __init__(self):
		super(RunCommand, self).__init__()
		self.main_command = "docker run"

		## RunCommand Filters for configuration file values
		self.filters = ["expose", "mount", "link"]

		self.__printer = Printer()

	def filter_expose(self, param, container = None):
		""" filter -p param for docker run """

		port_list = []
		for port in param[1]:
			port_list += ["-p", port]
		
		return port_list

	def filter_mount(self, param, container = None):
		""" filter -v param for docker run """

		## Need to add some exception handling here
		## Just to ensure we have a container here
		mount_list = []
		for mount in param[1]:
			mount_split = mount.split(':')
			mount_split[0] = os.path.abspath(container.path + '/' + mount_split[0])
			mount_list += ["-v", str.join(':', mount_split)]

		return mount_list

	def filter_link(self, param, container = None):
		""" filter --link param for docker run """

		share_list = []
		for share in param[1]:
			share_list += ["--link", "raiden-application-" + share + ":" + share]

		return share_list

	def execute(self, container):
		"""
			Execute command, 4 possible way of execution depending of container state :
				- Container is already running. Do nothing
				- Container is stopped. Just resume it.
				- Container doesn't exists, but his image do. Run it for the first time using configuration file and docker run.
				- Container doesn't exists, not his image. We need to build it and then run it for the first rime.
			Since we don't have any triggers yet in Raiden, we do the logic here. Won't stay here for too long.
		"""

		## Already running ? Nothing to do then ...
		if container.status == container.STATUS_RUNNING:
			self.__printer.info("Run", "Container " + container.internal_name + " already running")
			return self.RETURN_WONT_DO

		## Container's image is not build, so we build it
		if container.status == container.STATUS_UNKNOWN:
			self.__printer.info("Run", "Building image " + container.internal_image_name)
			self.__printer.debug("Run", "Executing 'build -t " + container.internal_image_name + " " + container.dockerfile + "'")
			DEVNULL = open(os.devnull, 'wb')
			subprocess.call(['docker', 'build', '-t', container.internal_image_name, container.dockerfile], stdout=DEVNULL, stderr=DEVNULL)
			DEVNULL.close()

		## To go any further, image must be runnable
		if not container.runnable:
			return self.RETURN_SUCCESS

		## Container is stopped, just need to resume it
		if container.status == container.STATUS_STOPPED:
			self.__printer.info("Run", "Resuming container " + container.internal_name)
			self.main_command = "docker start"
			self.params.append(container.internal_name)
			return super(RunCommand, self).execute(container)
		
		## Default behavior, we run container from configuration file
		self.__printer.info("Run", "Running container " + container.internal_name)
		
		## Adding params
		self.addParams(container.options, container)
		self.params += ["-d", "--name", container.internal_name, container.internal_image_name]

		return super(RunCommand, self).execute(container)