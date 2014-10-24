from base_filter import BaseFilter

class NameFilter(BaseFilter):
	"""
		Filter containers by name. This filter will consider container as valid only if name is in list.
	"""

	def filter(self, container):
		""" Perform filtering, return True if founded container is valid """

		if not container.name in self.values:
			return False

		return True