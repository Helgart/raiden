import os
import subprocess
from container.platform import Platform
from container.application import Application

class Finder:
    """ Run all dockers container in project folder """

    def __init__(self, root):
        ## Raiden root path
        self.__root = root

        ## Platform modules root path
        self.__platform_path = self.root + "/platform"

        ## Applications path
        self.__applications_path = self.root + "/applications"

        ## All founded platform modules
        ## These are Module object
        self.__platform_modules = []

        ## All founded applications
        ## These are Application object 
        self.__applications = []

    def searchPlatforms(self):
        """ Search for all platform docker containers in defined paths """

        ## Searching for plateform modules
        for module in os.listdir(self.platform_path):
            print "Checking " + self.platform_path + "/" + module
            if os.path.isfile(self.platform_path + "/" + module + "/config.yml"):
                container = Platform(self.platform_path + "/" + module, self.platform_path + "/" + module + "/config.yml")
            else:
                container = Platform(self.platform_path + "/" + module)
            self.__platform_modules.append(container)

        return self.platform_modules

    def searchApplications(self):
        """ Search for all applications docker containers in defined paths """

        ## Searching for application
        for application in os.listdir(self.applications_path):
            print "Checking " + self.applications_path + "/" + application
            if os.path.isfile(self.applications_path + "/" + application + "/config.yml"):
                container = Application(self.applications_path + "/" + application, self.applications_path + "/" + application + "/config.yml")
            else:
                container = Application(self.applications_path + "/" + application)
            self.__applications.append(container)

        return self.applications

    def search(self):
        """ Search for all docker containers in defined paths """

        return self.searchPlatforms(), self.searchApplications()

    ##
    ## Getters and setters definition
    ##

    @property
    def root(self):
        return self.__root

    @property
    def platform_path(self):
        return self.__platform_path

    @property
    def applications_path(self):
        return self.__applications_path

    @property
    def platform_modules(self):
        return self.__platform_modules

    @property
    def applications(self):
        return self.__applications

    @platform_path.setter
    def platform_path(self, value):
        self.__platform_path = value

    @applications_path.setter
    def applications_path(self, value):
        self.__applications_path = value