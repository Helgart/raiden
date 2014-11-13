import os
import importlib

from launcher.utilities.printer import Printer
from launcher.image_loader import ImageLoader

class Finder:
	"""
		Run all dockers container in project folder
		All of this is purely temporary, waiting for a proper finder implementation
	"""

	def __init__(self):
		self.filters = []
		self.targets = None

	def search(self, paths):
		""" Perform search in all paths """

		containers = {}
		containersList = []

		for path in paths:
			containersInPath = self.searchInPath(path)
			if containersInPath:
				containers = dict(containersInPath.items() + containers.items())

		## remove unused containers if targets are set
		containers = self.filterUnused(containers)

		for key,container in containers.items():
			containersList.append(container)

		return containersList

	def findDependencies(self, target, containers, usedOnes = {}):
		""" Recursivelly checking for dependencies """

		if target in usedOnes:
			return {}

		containersBuffer = {}

		if containers[target]:

			dependencies = []
			containersBuffer[target] = containers[target]

			if containers[target].options.has_key('depend'):
				dependencies = containers[target].options['depend']
			if containers[target].options.has_key('link'):
				dependencies += containers[target].options['link']
			if containers[target].options.has_key('persist'):
				dependencies += containers[target].options['persist']

			for dependency in dependencies:
				containersBuffer = dict(containersBuffer.items() + self.findDependencies(dependency, containers, containersBuffer).items())

		return containersBuffer
			

	def filterUnused(self, containers):
		""" If targets is defined, remove unused containers """

		## Well ... nothing to filter so we use all images
		if self.targets == None:
			return containers

		printer = Printer()
		usedOnes = {}

		for target in self.targets:

			## Finder can't resolve targets
			if not target in containers:
				printer.error("Finder", "Can't find " + target)
				continue

			usedOnes = dict(usedOnes.items() + self.findDependencies(target, containers).items())

		return usedOnes


	def searchInPath(self, path):
		""" Search for all platform docker containers in a defined paths """

		printer = Printer()
		containersInPath = {}
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
						containersInPath[container.name] = container
					else :
						printer.debug('Finder', 'Container ' + container.name + ' filtered')

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