import importlib

class Runner:
	""" Run a collection of containers """

	def run(self, containers, action):
		""" Run a collection of containers """

		ordered_containers = sorted(containers, key=lambda x: x.order)
		for container in ordered_containers:

			## We try to execute requested action
			try:
				command_module = importlib.import_module("launcher.commands." + action + "_command")
				command_class = getattr(command_module, action.title() + "Command")
				command = command_class()

				## Adding params
				command.addParams(container.options)

				## Executing command
				command.execute(container)

			except AttributeError as e:
				print e
				print "Unkown command " + action + " for container " + container.name
				return False

			return True