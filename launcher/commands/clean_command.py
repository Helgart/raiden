from base_command import BaseCommand
from stop_command import StopCommand

from launcher.utilities.printer import Printer

class CleanCommand(BaseCommand):
	""" Stop container and remove it """

	def __init__(self, force = False):
		super(CleanCommand, self).__init__(force)
		self.main_command = "docker rm"

		self.__printer = Printer()

	def manage_output(self, returncode, stdout, stderr):
		""" Manage command output """

		if returncode == 1:
			return 0

		return super(CleanCommand, self).manage_output(returncode, stdout, stderr)

	def execute(self, container):
		""" Stop container if running and remove it """

		## First, we stop the container if container is runnable
		if container.runnable:
			stop_command = StopCommand()
			return_value = stop_command.execute(container)

		## We must check if this container is secured and must not be removed without force option
		if not container.removable and not self.force:
			self.__printer.debug("Run", "Container " + container.internal_name + " is protected and can't be deleted")
			return

		if not container.removable and self.force:
			self.__printer.info("Run", "Force removing " + container.internal_name)

		## Something happend while stopping container
		## so we need to stop here
		## Well ... Later I'll have to add some force parameter
		if return_value:
			self.__printer.warning("Clean", "Oops, seems like we can't stop container")
			return self.RETURN_WONT_DO
		
		self.__printer.info("Clean", "Cleaning " + container.internal_name)
		self.params.append(container.internal_name)
		return super(CleanCommand, self).execute(container)