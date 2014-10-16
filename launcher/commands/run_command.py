import os
import subprocess

from base_command import BaseCommand

## @todo In next step, some trigger using container inspect would be nice !
class RunCommand(BaseCommand):
	""" Build a docker command from command type and configuration """

	def __init__(self):
		super(RunCommand, self).__init__()
		self.main_command = "docker run"

		## RunCommand Filters for configuration file values
		self.filters = ["detached", "interactive", "tty", "expose"]

	def filter_detached(self, param):
		""" filter -d param for docker run """

		if param:
			return "-d"
		return None

	def filter_tty(self, param):
		""" filter -t param for docker run """

		if param:
			return "-t"
		return None

	def filter_expose(self, param):
		""" filter -p param for docker run """

		port_list = []
		for port in param[1]:
			port_list += ["-p", port]
		
		return port_list

	def filter_interactive(self, param):
		""" filter -i param for docker run """

		if param:
			return "-i"
		return None

	def execute(self, container):
		"""
			Execute command, 4 possible way of execution depending of container state :
				- Container is already running. Do nothing
				- Container is stopped. Just resume it.
				- Container doesn't exists, but his image do. Run it for the first time using configuration file and docker run.
				- Container doesn't exists, not his image. We need to build it and then run it for the first rime.
			Since we don't have any triggers yet in Raiden, we do the logic here. Won't stay here for too long.
		"""

		if container.status == container.STATUS_RUNNING:
			print "Container " + container.internal_name + " already running"
			return self.RETURN_WONT_DO

		if container.status == container.STATUS_UNKNOWN:
			print "Image " + container.internal_image_name + " need to be build, won't do for now"
			return self.RETURN_WONT_DO

		if container.status == container.STATUS_STOPPED:
			print "Resuming container " + container.internal_name
			self.main_command = "docker start"
			self.params = [container.internal_name]
		elif container.status == container.STATUS_BUILD:
			print "Running container " + container.internal_name
			self.params += ["--name", container.internal_name, container.internal_image_name]
		else:
			print "Unknown status"
			return self.RETURN_WONT_DO
		
		return_code = super(RunCommand, self).execute(container)

		if return_code != 0:
			print "Failed to run " + container.internal_name
			return return_code

		return self.RETURN_SUCCESS