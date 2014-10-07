import os
import subprocess

######################
## Run all dockers container in project folder
## 
## Just a POC for now, if ok will be separate in separate files
######################

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
        subprocess.call(['docker', 'run', '-ti', '-p', '80:80', '--name', container_name, image_name], stdout=DEVNULL, stderr=DEVNULL)
        return True
    print "Starting container " + container_name
    subprocess.call(['docker', 'start', container_name], stdout=DEVNULL, stderr=DEVNULL)
    return True

def load(modules):
    for module in os.listdir(modules):
        print "Checking " + modules + "/" + module + "/Dockerfile"
        builtImage(modules + "/" + module, "raiden-" + module + "-image")
        runContainer("raiden-" + module, "raiden-" + module + "-image")
