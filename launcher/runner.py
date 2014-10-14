class Runner:
	""" Run a collection of containers """

	def run(self, containers, action):
		""" Run a collection of containers """

		ordered_containers = sorted(containers, key=lambda x: x.order)
		for container in ordered_containers:
			
			## We try to execute requested action
			try:
				action_method = getattr(container, action)
			except AttributeError:
				print "Unknown action " + action + " for container " + container.name
				return False

			## Here will be builded some parameters to pass to the container action
			action_method()

			return True