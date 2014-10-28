from base_container import BaseContainer

class Layer(BaseContainer):
	""" A simple layer image, we can build the image, but not run it """

	def __init__(self, path, configuration = None):
		super(Layer, self).__init__(path, configuration)
		self.__runnable = False