import importlib
from utilities.printer import Printer

class Runner:
	""" Run a collection of containers """

	def run(self, containers, action):
		""" Run a collection of containers """

		printer = Printer()
		ordered_containers = sorted(containers, key=lambda x: x.order)
		for container in ordered_containers:

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
