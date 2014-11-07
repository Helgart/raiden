from base_command import BaseCommand
from clean_command import CleanCommand

from launcher.utilities.printer import Printer

class CleanImageCommand(BaseCommand):
	""" Stop container and remove it """

	def __init__(self):
		super(CleanImageCommand, self).__init__()
		self.main_command = "docker rmi"

		self.__printer = Printer()

	def manage_output(self, returncode, stdout, stderr):
		""" Manage command output """

		if returncode == 1:
			return 0

		return super(CleanImageCommand, self).manage_output(returncode, stdout, stderr)

	def execute(self, container):
		""" Stop container if running and remove it """

		## First, we clean the container
		clean_command = CleanCommand()
		return_value = clean_command.execute(container)

		self.params.append(container.internal_image_name)		
		result = super(CleanImageCommand, self).execute(container)

		self.__printer.info("Clean", "Cleaning image " + container.internal_image_name)
		return result