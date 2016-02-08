from basic_operations import BasicOperations
from image_operations import ImageOperations
from container_operations import ContainerOperations


class DockerManager(BasicOperations, ImageOperations, ContainerOperations):
    """

    :param str host: Docker host url to connect to deamon.
    :param bool tls_verify: TLS configiration(Default is False).
    :param pem cert: Certificate file cert(Default is None).
    :param pem key: Certificate file key(Default is None).
    :param pem ca: Certificate file to verify(Default is None).

    By instantiating a DockerManager object, you can able to communicate with Docker deamon::
 
    >>>from docker_manager import DockerManager
    >>>docker_manager = DockerManager(host='docker.marlabs.com:2376',\
        tls_verify=True,cert='/cert/cert.pem',key='/cert/key.pem',ca='/cert/ca.pem')
    >>>docker_manager.ping()
    
    """

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
    
        super(DockerManager, self).__init__(host, tls_verify, cert, key, ca)

