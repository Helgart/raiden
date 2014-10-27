import importlib

from utilities.printer import Printer

class Runner:
	""" Run a collection of containers """

	def __init__(self, env = None):
		self.env = env

	def __elementIsSorted(self, name, sortedList):
		""" Check if container has already been sorted """

		for element in sortedList:
			if element.name == name:
				return True

		return False

	def toposort(self, containers):
		"""
			Toposort of containers:
			Compare container name to container links.
			Throw an exception if we have circular dependencies.
		"""

		unsorted_containers = containers
		sorted_containers = []

		index = 0
		unsorted_containers_length = len(unsorted_containers)
		while unsorted_containers_length and index < unsorted_containers_length:

			resolved = False

			## Case if a container has no dependencies
			## We can directly push it to the sorted list
			if not containers[index].options.has_key('link'):
				resolved = True

			## So the container has dependencies,
			## we need to check if they're resolved
			if not resolved:
				resolved = True
				for link in containers[index].options['link']:
					if not self.__elementIsSorted(link, sorted_containers):
						resolved = False
						break

			## Dependency is resolved !
			## Cool, let's add it to the sorted list
			if resolved:
				sorted_containers.append(containers[index])
				del unsorted_containers[index]
				index = 0
				unsorted_containers_length = len(unsorted_containers)

			## We couldn't resolve dependencies so we continue iteration
			else:
				index += 1

		if len(unsorted_containers):
			raise Exception("Can't resolve dependencies")

		return sorted_containers

	def run(self, containers, action):
		""" Run a collection of containers """

		printer = Printer()
		
		## We try to sort containers to resolve dependencies
		try:
			containers = self.toposort(containers)
		except Exception as e:
			printer.error("Runner", e.message)
			return False

		for container in containers:

			container.currentEnv = self.env

			## We try to execute requested action
			try:
				command_module = importlib.import_module("launcher.commands." + action + "_command")
				command_class = getattr(command_module, action.title() + "Command")
				command = command_class()

				## Executing command
				return_code = command.execute(container)

				if return_code:
					printer.error("Runner", "Failed to execute action " + action + " on container " + container.name)

			except AttributeError as e:
				print e
				print "Unkown command " + action + " for container " + container.name
				return False

		return True
