import os
import subprocess
from image_loader import ImageLoader

class Finder:
    """ Run all dockers container in project folder """

    def search(self, path):
        """ Search for all platform docker containers in defined paths """

        images = []
        loader = ImageLoader()

        ## Searching for plateform modules
        for image in os.listdir(path):
            if os.path.isdir(path + "/" + image):
                print "Checking " + path + "/" + image
                if os.path.isfile(path + "/" + image + "/config.yml"):
                    container = loader.load(path + "/" + image)
                images.append(container)

        return images