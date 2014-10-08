import os
import subprocess

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

    def search(self):
        ## Searching for plateform modules
        for module in os.listdir(self.platform_path):
            print "Checking " + self.platform_path + "/" + module + "/Dockerfile"
        
        ## Searching for application
        for application in os.listdir(self.applications_path):
            print "Checking " + self.applications_path + "/" + application + "/Dockerfile"

            ## To be replaced by an Image object
            #builtImage(modules + "/" + module, "raiden-" + module + "-image")

            ## To be replaced by a Container object
            #runContainer("raiden-" + module, "raiden-" + module + "-image")

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










#####
## Just for reference
#####

def imageIsBuilt(image_name):
    DEVNULL = open(os.devnull, 'wb')
    docker_images = subprocess.Popen(['docker', 'images'], stdout=subprocess.PIPE)
    if subprocess.call(['grep', image_name], stdin=docker_images.stdout, stdout=DEVNULL, stderr=DEVNULL):
        return False
    return True

def builtImage(path, image_name):
    DEVNULL = open(os.devnull, 'wb')
    if not imageIsBuilt(image_name) and os.path.exists(path + "/Dockerfile"):
        print "Building " + image_name + " from file " + path + "/Dockerfile"
        subprocess.call(["docker", "build", "-t", image_name, path], stdout=DEVNULL, stderr=DEVNULL)

## containerIsRunning and containerExists should be reunit in one method
## -> containerStatus

def containerIsRunning(container_name):
    DEVNULL = open(os.devnull, 'wb')
    docker_containers = subprocess.Popen(['docker', 'ps'], stdout=subprocess.PIPE)
    if subprocess.call(['grep', container_name], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
        return False
    return True

def containerExists(container_name):
    DEVNULL = open(os.devnull, 'wb')
    docker_containers = subprocess.Popen(['docker', 'ps', '-a'], stdout=subprocess.PIPE)
    if subprocess.call(['grep', container_name], stdin=docker_containers.stdout, stdout=DEVNULL, stderr=DEVNULL):
        return False
    return True

## Run the container
## Well, we should have some configuration files to set how we should run the container

def runContainer(container_name, image_name):
    DEVNULL = open(os.devnull, 'wb')
    if containerIsRunning(container_name):
        print "Container " + container_name + " is already running"
        return False
    if not containerExists(container_name):
        print "Launching " + container_name + " using image " + image_name
        subprocess.call(['docker', 'run', '-tid', '-p', '80:80', '--name', container_name, image_name], stdout=DEVNULL, stderr=DEVNULL)
        return True
    print "Starting container " + container_name
    subprocess.call(['docker', 'start', container_name], stdout=DEVNULL, stderr=DEVNULL)
    return True