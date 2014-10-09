class Runner:
	""" Run a collection of containers """

	def run(self, containers):
		""" Run a collection of containers """

		ordered_containers = sorted(containers, key=lambda x: x.order)
		for container in ordered_containers:
			container_status = container.status()
			if container_status == container.UNDEFINED:
				container.build()
			container.run()