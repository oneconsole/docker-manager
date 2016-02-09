from docker_server import DockerServer
from constants import DockerEndPoint


class ImageOperations(DockerServer):

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
        super(ImageOperations, self).__init__(host, tls_verify, cert, key, ca)

    def list_image(self, query_param=None):
        return self._get(DockerEndPoint.LIST_IMAGES, query_param)

    def delete_image(self, image_id, force_delete=False):
        query_param = {
            'force': force_delete
        }
        return self._delete(DockerEndPoint.REMOVE_IMAGE.format(image_id), query_param)

    def get_image_detail(self, image_id):
        return self._get(DockerEndPoint.INSPECT_IMAGE.format(image_id))
    
    def get_image_history(self, image_id):
        return self._get(DockerEndPoint.IMAGE_HISTORY.format(image_id))

    def search_image(self, search_name):
        return self._get(DockerEndPoint.SEARCH_IMAGE.format(search_name))

    def get_image_tags(self, image_name):
        response = requests.get(DockerEndPoint.IMAGE_TAGS.format(image_name))
        return self._prepare_response_content(response)

    def download_image(self, image_name, tag=None, source=None, repo=None, registry=None):
        data = {
            'fromImage': image_name,
            'tag': tag,
            'fromSrc': source,
            'repo': repo,
            'registry': registry
        }
        return self._post(DockerEndPoint.CREATE_IMAGE, data)

    def push_image(self, repo_name, headers, tag=None):
        data = {
            'tag': tag
        }
        return self._post(DockerEndPoint.PUSH_IMAGE, headers=headers, data=data)
