from docker_server import DockerServer
from constants import DockerEndPoint


class BasicOperations(DockerServer):

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
        super(BasicOperations, self).__init__(host, tls_verify, cert, key, ca)
        
    def ping(self):
        """Ping the docker deamon::
     
        >>>docker = DockerManager(host='docker.marlabs.com:2376')
        >>>docker.ping()
        >>>{'content': 'OK', 'status': True}

        """
        return self._get(DockerEndPoint.PING)

    def get_info(self):
        """Get the basic docker info::
     
        >>>docker = DockerManager(host='docker.marlabs.com:2376')
        >>>docker.get_info()

        """
        return self._get(DockerEndPoint.INFO)

    def get_version(self):
        """Get Docker version::
     
        >>>docker = DockerManager(host='docker.marlabs.com:2376')
        >>>docker.get_version()

        """
        return self._get(DockerEndPoint.VERSION)