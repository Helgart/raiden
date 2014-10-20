from base_command import BaseCommand
from stop_command import StopCommand

from launcher.utilities.printer import Printer

class CleanCommand(BaseCommand):
	""" Stop container and remove it """

	def __init__(self):
		super(CleanCommand, self).__init__()
		self.main_command = "docker rm"

		self.__printer = Printer()

	def execute(self, container):
		""" Stop container if running and remove it """

		## First, we stop the container
		stop_command = StopCommand()
		return_value = stop_command.execute(container)

		## Something happend while stopping container
		## so we need to stop here
		## Well ... Later I'll have to add some force parameter
		if return_value:
			self.__printer.warning("Clean", "Oops, seems like we can't stop container")
			return self.RETURN_WONT_DO
		
		self.__printer.info("Clean", "Cleaning " + container.internal_name)
		self.params.append(container.internal_name)
		return super(CleanCommand, self).execute(container)