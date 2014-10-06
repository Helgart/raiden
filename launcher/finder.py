import os

def load(modules):
    for module in os.listdir(modules):
        print "Checking " + modules + "/" + module + "/Dockerfile"
        if os.path.exists(modules + "/" + module + "/Dockerfile"):
            print "Launching " + module + " with file " + modules + "/" + module + "/Dockerfile"
		#os.system("docker build -t raiden " + path + "/nginx")
		#os.system("docker run --name raiden -ti -p 80:80")
