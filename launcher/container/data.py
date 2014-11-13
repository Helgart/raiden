from base_container import BaseContainer

class Data(BaseContainer):
	"""
		A simple Data persistent image, we can build the image, but not run it.
		Furthermore, you must confirm instance deletion with --with-data option
	"""

	def __init__(self, path, configuration = None):
		super(Data, self).__init__(path, configuration)
		self.removable = False
		self.autorun = False