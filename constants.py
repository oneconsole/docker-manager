from utils import BaseEnum


class DockerEndPointEnum(BaseEnum):

    def __init__(self):

        # Basic
        self.PING = '/_ping'
        self.INFO = '/info'
        self.VERSION = '/version'

        # Containers
        self.LIST_CONTAINER = '/containers/json'
        self.INSPECT_CONTAINER = '/containers/{0}/json'        
        self.CREATE_CONTAINER = '/containers/create'
        self.CONTAINER_OPERATION = '/containers/{0}/{1}'
        self.REMOVE_CONTAINER = '/containers/{0}'
        self.COMMIT_CONTAINER = '/commit{0}'
        self.CONTAINER_STATS = '/containers/{0}/stats'
        self.CONTAINER_LOGS = '/containers/{0}/logs'        
        self.CONTAINER_PROCESS_LIST = '/containers/{0}/top'

        # Images
        self.LIST_IMAGES = '/images/json'
        self.REMOVE_IMAGE = '/images/{0}'
        self.INSPECT_IMAGE = '/images/{0}/json'
        self.IMAGE_HISTORY = '/images/{0}/history'
        self.SEARCH_IMAGE = '/images/search?term={0}'
        self.CREATE_IMAGE = '/images/create'
        self.PUSH_IMAGE = '/images/{0}/push{1}'

        # docker registry
        self.DOCKER_REGISTRY = 'https://registry.hub.docker.com/v1/repositories/'
        self.IMAGE_TAGS = self.DOCKER_REGISTRY + '{0}/tags'


DockerEndPoint = DockerEndPointEnum()


# class ContainerTranformTypeEnum(BaseEnum):

#     def __init__(self):
#         self.COMPOSE = 'compose'
#         self.ECS = 'ecs'

# ContainerTranformType = ContainerTranformTypeEnum()


class WebConnectionTypeEnum(BaseEnum):

    def __init__(self):
        self.SECURE = 'https://'
        self.INSECURE = 'http://'

WebConnectionType = WebConnectionTypeEnum()


class WebResponseStatusCodeEnum(BaseEnum):

    def __init__(self):
        self.SUCCESS_LIST = [200, 201, 204]
        self.ERROR_LIST = [404, 409, 500]

WebResponseStatusCode = WebResponseStatusCodeEnum()


class ContainerOperationEnum(BaseEnum):

    def __init__(self):
        self.START = 'start'
        self.STOP = 'stop'
        self.RESTART = 'restart'
        self.PAUSE = 'pause'
        self.UNPAUSE = 'unpause'
        self.RENAME = 'rename'

ContainerOperation = ContainerOperationEnum()
