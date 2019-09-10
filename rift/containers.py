import docker

# Connect to Docker Daemon
client = docker.from_env()

class Container:

    list = []

    def __init__(self, label, cid):
        self.label = label
        self.cid = cid
        try:
            self.container = client.containers.get(self.cid)
        except docker.errors.NotFound as error:
            print("[!] Docker container '" + cid + "' requested but not found.")
            self.container = None
        self.__class__.list.append(self)

    @property
    def status(self):
        self.container.reload()
        return self.container.status

    @property
    def isRunning(self):
        self.container.reload()
        if self.status == "running": 
            return True 
        else: 
            return False

# Get MongoDB Container #TODO Do not hardcode docker container ID.
# This is for testing only. Program will fail if this is not the MongoDB cid.
mongo = Container("MongoDB", 'rift_database')