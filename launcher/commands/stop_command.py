from base_command import BaseCommand

class StopCommand(BaseCommand):
	""" Stop containers """

	def __init__(self):
		super(StopCommand, self).__init__()
		self.main_command = "docker stop"

	def execute(self, container):
		""" Stop container if running """

		if not container.status == container.STATUS_RUNNING:
			print "Container " + container.internal_name + " is not running"
			return self.RETURN_SUCCESS

		print "Stopping " + container.internal_name
		self.params.append(container.internal_name)
		
		return super(StopCommand, self).execute(container)