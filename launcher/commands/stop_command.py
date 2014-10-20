from base_command import BaseCommand

from launcher.utilities.printer import Printer

class StopCommand(BaseCommand):
	""" Stop containers """

	def __init__(self):
		super(StopCommand, self).__init__()
		self.main_command = "docker stop"

		self.__printer = Printer()

	def execute(self, container):
		""" Stop container if running """

		if not container.status == container.STATUS_RUNNING:
			self.__printer.info("Stop", "Container " + container.internal_name + " is not running")
			return self.RETURN_SUCCESS

		self.__printer.info("Stop", "Stopping " + container.internal_name)
		self.params.append(container.internal_name)
		
		return super(StopCommand, self).execute(container)