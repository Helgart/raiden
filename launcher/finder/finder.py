import os
import importlib

from launcher.utilities.printer import Printer
from launcher.image_loader import ImageLoader

class Finder:
	""" Run all dockers container in project folder """

	def __init__(self):
		self.filters = []

	def search(self, path):
		""" Search for all platform docker containers in defined paths """

		printer = Printer()
		images = []
		loader = ImageLoader()

		printer.debug("Finder", "Searching for docker instances in " + path)

		## Searching for plateform modules
		for image in os.listdir(path):
			if os.path.isdir(path + "/" + image):
				printer.debug("Finder", "Checking " + path + "/" + image)
				if os.path.isfile(path + "/" + image + "/config.yml"):
					container = loader.load(path + "/" + image)

					## Filtering loaded container
					## No action must be performed on that container if filtered
					if self.filter(container):
						printer.info('Finder', 'Container ' + container.name + ' filtered')
						images.append(container)

		return images

	def filter(self, container):
		""" Filter container, return True if container is valid """

		for filter_object in self.filters:
			if filter_object.filter(container):
				return False
		return True

	def addFilter(self, name, values):
		""" Try to add requested filter in list """

		## Try to instanciate filter
		try:
			filter_module = importlib.import_module("launcher.finder.finder_filter." + name + "_filter")
			filter_class = getattr(filter_module, name.title() + "Filter")
			filter_instance = filter_class()

			## storing filter
			filter_instance.values = values
			self.filters.append(filter_instance)
			

		except AttributeError as e:
			print e
			print "Unkown filter " + name
			return False

		return True