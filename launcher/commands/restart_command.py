from base_command import BaseCommand
from stop_command import StopCommand
from run_command import RunCommand

class RestartCommand(BaseCommand):
	""" restart container """

	def __init__(self):
		super(RestartCommand, self).__init__()

	def execute(self, container):
		"""
			Restart container if running, depend on 2 commands :
				- StopCommand : to stop container
				- RunCommand : to start container
		"""

		## First, we stop the container
		stop_command = StopCommand()
		return_value = stop_command.execute(container)
		
		## Something happend while stopping container
		## so we need to stop here
		if return_value:
			print "Oops, seems like we can't stop container"
			return self.RETURN_WONT_DO

		# refreshing container status
		container.refresh_status()
		
		## Everything's fine, let's start this again
		run_command = RunCommand()
		run_command.execute(container)	
		
		return self.RETURN_SUCCESS