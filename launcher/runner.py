import importlib

from utilities.printer import Printer

class Runner:
	""" Run a collection of containers """

	def __init__(self, env = None, force = False):
		self.env = env
		self.force = force

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
			## Will be independant containers or layers
			if not containers[index].options.has_key('link') and not containers[index].options.has_key('depend') and not containers[index].options.has_key('persist'):
				resolved = True

			## So the container has dependencies,
			## we need to check if they're resolved
			if not resolved:
				resolved = True
				if containers[index].options.has_key('depend'):
					for dependency in containers[index].options['depend']:
						if not self.__elementIsSorted(dependency, sorted_containers):
							resolved = False
							break
				elif containers[index].options.has_key('persist'):
					for persistent in containers[index].options['persist']:
						if not self.__elementIsSorted(persistent, sorted_containers):
							resolved = False
							break
				else:
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
			raise Exception("Can't resolve dependencies for containers : " + str(map(lambda x: x.name, unsorted_containers)))

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

		## Some logic with toposort will be change in 0.3-beta
		## But right now here a small fix to fix dependencies with clean commands
		if action == 'clean' or action == 'clean-image' :
			containers = reversed(containers)

		## For now, just a simple error handling
		## Will be improved in next version
		has_errors = False

		for container in containers:

			container.currentEnv = self.env

			## We try to execute requested action
			try:
				# Some sanity treatment
				command_names = action.split('-')
				command_module_name = "launcher.commands." + '_'.join(command_names) + "_command"
				command_class_name = ''.join(map(lambda x: x.title(), command_names)) + 'Command'

				command_module = importlib.import_module(command_module_name)
				command_class = getattr(command_module, command_class_name)
				command = command_class(self.force)

				## Executing command
				return_code = command.execute(container)

				if return_code:
					printer.error("Runner", "Failed to execute action " + action + " on container " + container.name)
					has_errors = True

			except AttributeError as e:
				print e
				print "Unkown command " + action + " for container " + container.name
				return False

		return has_errors
