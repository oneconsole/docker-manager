import requests
from constants import WebConnectionType, WebResponseStatusCode


class DockerServer(object):

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
        self.host = host
        self.tls_verify = tls_verify
        self.cert = cert
        self.key = key
        self.ca = ca

    def _prepare_url(self, end_point):
        if self.tls_verify:
            return WebConnectionType.SECURE + self.host + end_point
        else:
            return WebConnectionType.INSECURE + self.host + end_point

    def _get(self, end_point, params=None, headers=None, stream=False):
        try:
            url = self._prepare_url(end_point)
            response = requests.get(
                url=url,
                params=params,
                headers=headers,
                stream=stream,
                cert=(self.cert, self.key),
                verify=self.ca,
                timeout=5
            )
        except Exception as e:
            raise
        return self._prepare_response_content(response, stream=stream)

    def _post(self, end_point, data=None, headers=None):
        try:
            url = self._prepare_url(end_point)
            response = requests.post(
                url=url,
                data=data,
                headers=headers,
                cert=(self.cert, self.key),
                verify=self.ca,
                timeout=5
            )
        except Exception as e:
            raise
        return self._prepare_response_content(response)

    def _delete(self, end_point, data=None):
        try:
            url = self._prepare_url(end_point)
            response = requests.delete(
                url=url,
                data=data,
                cert=(self.cert, self.key),
                verify=self.ca,
                timeout=5
            )
        except Exception as e:
            raise
        return self._prepare_response_content(response)

    def _prepare_response_content(self, response, stream=False):
        if response.status_code in WebResponseStatusCode.SUCCESS_LIST:
            try:
                if stream:
                    content = response.iter_lines()
                elif 'application/json' in response.headers['content-type']:
                    content = response.json()
                else:
                    content = response.content
            except:
                content = response.content
            response_content = {
                'status': True,
                'content': content
            }
        else:
            response_content = {
                'status': False,
                'content': response.content
            }
        return response_content
