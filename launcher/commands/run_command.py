from base_command import BaseCommand

class RunCommand(BaseCommand):
	""" Build a docker command from command type and configuration """

	def __init__(self):
		super(RunCommand, self).__init__()
		self.main_command = "docker run"

		## RunCommand Filters for configuration file values
		self.filters = ["detached", "interactive", "tty", "expose"]

	def filter_detached(self, param):
		""" filter -d param for docker run """

		if param:
			return "-d"
		return None

	def filter_tty(self, param):
		""" filter -t param for docker run """

		if param:
			return "-t"
		return None

	def filter_expose(self, param):
		""" filter -p param for docker run """

		return ["-p"] + param[1]

	def filter_interactive(self, param):
		""" filter -i param for docker run """

		if param:
			return "-i"
		return None

	def execute(self, container):
		""" Execute command """

		self.params += ["--name", container.internal_name, container.internal_image_name]
		super(RunCommand, self).execute(container)