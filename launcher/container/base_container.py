import os
import subprocess
import yaml
import json

## @todo: mainly missing some log
## @todo: no additional parameters for now, to add
class BaseContainer:
	""" Base container, herited by all container types """

	def __init__(self, path, configuration = None):
		""" load default attributes """

		self.__name = ''
		self.__order = 0
		self.__options = []
		self.__inspect = None
		self.__path = path

		self.init(configuration)
		self.__internal_name = "raiden-" + self.name
		self.__internal_image_name = "raiden-" + self.name + "-image"

	def init(self, configuration):
		""" Init the container object using configuration object """

		self.__name = configuration['name']
		self.__order = configuration['order']
		self.__options = configuration['options']

	##
	## Getters and Setters definition
	##

	@property
	def name(self):
		return self.__name

	@property
	def internal_name(self):
		return self.__internal_name

	@property
	def internal_image_name(self):
		return self.__internal_image_name

	@property
	def order(self):
		return self.__order

	@property
	def options(self):
		return self.__options

	@property
	def path(self):
		return self.__path
