import os
import importlib

from launcher.utilities.printer import Printer
from launcher.image_loader import ImageLoader

class Finder:
	""" Run all dockers container in project folder """

	def __init__(self):
		self.filters = []

	def search(self, paths):
		""" Perform search in all paths """

		containers = []

		for path in paths:
			containersInPath = self.searchInPath(path)
			if containersInPath:
				containers += containersInPath

		return containers

	def searchInPath(self, path):
		""" Search for all platform docker containers in a defined paths """

		printer = Printer()
		containersInPath = []
		loader = ImageLoader()

		printer.debug("Finder", "Searching for docker instances in " + path)

		## Searching for plateform modules
		for image in os.listdir(path):
			if os.path.isdir(path + "/" + image):
				printer.debug("Finder", "Checking " + path + "/" + image)
				if os.path.isfile(path + "/" + image + "/raiden.yml"):
					container = loader.load(path + "/" + image)

					## Filtering loaded container
					## No action must be performed on that container if filtered
					if self.filter(container):
						containersInPath.append(container)
					else :
						printer.info('Finder', 'Container ' + container.name + ' filtered')

		return containersInPath

	def filter(self, container):
		""" Filter container, return True if container is valid """

		for filter_object in self.filters:
			if not filter_object.filter(container):
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
			print "Unkown filter " + name
			return False

		return True