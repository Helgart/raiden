from base_command import BaseCommand

from launcher.utilities.printer import Printer

class RebuiltCommand(BaseCommand):
	""" Rebuilt image command """

	def __init__(self):
		super(RebuiltCommand, self).__init__()
		self.main_command = "docker build"

		self.__printer = Printer()

	def execute(self, container):
		""" Rebuilt an image """

		self.params += ['-t', container.internal_image_name, container.dockerfile]

		self.__printer.info("Rebuilt", "Rebuilting image " + container.internal_image_name)
		return super(RebuiltCommand, self).execute(container)