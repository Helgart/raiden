class BaseFilter(object):
	"""
		Base filter class definition.
		Iherited filters are intented to be used by container finder (Finder) to filter results.
	"""

	def __init__(self):
		self.filters = []

	def filter(self, container):
		""" Perform filtering on a container, return True if founded container is valid """
		
		return True