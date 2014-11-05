from base_command import BaseCommand

from launcher.utilities.printer import Printer

class RebuildCommand(BaseCommand):
	""" Rebuild image command """

	def __init__(self):
		super(RebuildCommand, self).__init__()
		self.main_command = "docker build"

		self.__printer = Printer()

	def execute(self, container):
		""" Rebuild an image """

		self.params += ['-t', container.internal_image_name, container.dockerfile]

		self.__printer.info("Rebuild", "Rebuilding image " + container.internal_image_name)
		return super(RebuildCommand, self).execute(container)