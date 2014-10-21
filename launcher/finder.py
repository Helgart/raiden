import os
import subprocess

from utilities.printer import Printer
from image_loader import ImageLoader

class Finder:
	""" Run all dockers container in project folder """

	def search(self, path):
		""" Search for all platform docker containers in defined paths """

		printer = Printer()
		images = []
		loader = ImageLoader()

		printer.debug("Finder", "Searching for docker instances in " + path)

		## Searching for plateform modules
		for image in os.listdir(path):
			if os.path.isdir(path + "/" + image):
				printer.debug("Finder", "Checking " + path + "/" + image)
				if os.path.isfile(path + "/" + image + "/config.yml"):
					container = loader.load(path + "/" + image)
					images.append(container)

		return images