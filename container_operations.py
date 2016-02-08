from docker_server import DockerServer
from constants import DockerEndPoint, ContainerOperation
from utils import _multiplexed_buffer_helper


class ContainerOperations(DockerServer):

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
        super(ContainerOperations, self).__init__(host, tls_verify, cert, key, ca)

    def list_container(self, all=False, limit=None, since=None, before=None, size=False, filters=None):
        query_param = {
            'all': all,
            'limit': limit,
            'since': since,
            'before': before,
            'size': size,
            'filters': filters
        }
        return self._get(DockerEndPoint.LIST_CONTAINER, query_param)

    def inspect_container(self, container_id, raw_json=False):
        response = self._get(DockerEndPoint.INSPECT_CONTAINER.format(container_id))
        if raw_json and response['status']:
            return self._prepare_container_info_json(response['content'])
        return response

    def create_container_from_config(self, configuration, name=None):
        headers = {'content-type': 'application/json'}
        return self._post(''.join([DockerEndPoint.CREATE_CONTAINER, '?name=' + name if name else '']), configuration, headers)

    def start_container(self, container_id):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.START))

    def stop_container(self, container_id):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.STOP))

    def restart_container(self, container_id):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.RESTART))

    def pause_container(self, container_id):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.PAUSE))

    def unpause_container(self, container_id):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.UNPAUSE))

    def rename_container(self, container_id, name):
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.START), name)

    def remove_container(self, container_id, force=False, volume=False):
        params = {
            'force': force,
            'v': volume
        }
        return self._delete(DockerEndPoint.REMOVE_CONTAINER.format(container_id), params)

    def commit_container(self, container_id, image_name=None, tag=None, comment=None, author=None):
        query_param = "?container=" + container_id
        if image_name:
            query_param = query_param + "&repo=" + image_name
        if tag:
            query_param = query_param + "&tag=" + tag
        if comment:
            query_param = query_param + "&comment=" + comment
        if author:
            query_param = query_param + "&author=" + author
        return self._post(DockerEndPoint.COMMIT_CONTAINER.format(query_param))

    def get_container_statics(self, container_id):
        return self._get(DockerEndPoint.CONTAINER_STATS.format(container_id), stream=True)

    def get_container_logs(self, container_id, std_out=False, std_err=False, date_time=0, time_stamp=False, count=all):
        d = {'stdout': std_out, 'stderr': std_err, 'since': date_time, 'timestamps': time_stamp, 'tail': count}
        params = '&'.join(['{}={}'.format(k, v) for k, v in d.iteritems()])
        end_url = '?'.join([DockerEndPoint.CONTAINER_LOGS.format(container_id), params])
        response = self._get(end_url)
        response['content'] = ''.join([x for x in self._multiplexed_buffer_helper(response['content'])])
        return response

    def list_contaier_process(self, container_id, ps_args=None):
        end_url = DockerEndPoint.CONTAINER_PROCESS_LIST.format(container_id)
        if ps_args:
            end_url = end_url + '?ps_args=' + ps_args
        return self._get(end_url)

    def _prepare_container_info_json(self, content):
        created_date = content['Created'].split('.')
        created_date = created_date[0].split('T')
        content_json = {
            'Cont_Id': content['Id'],
            'Name': content['Name'].split('/')[1],
            'Image': content['Config']['Image'],
            'Created_date': created_date[0],
            'Created_time': created_date[1],
            'State_running': content['State']['Running'],
            'State_restarting': content['State']['Restarting'],
            'State_paused': content['State']['Paused'],
            'CpuShares': content['HostConfig']['CpuShares'],
            'Cpuset': content['HostConfig']['CpusetCpus'],
            'Links': content['HostConfig']['Links'],
            'Env': content['Config']['Env'],
            'VolumesFrom': content['HostConfig']['VolumesFrom'],
            'Volume': content['Config']['Volumes'],
            'Cmd': content['Config']['Cmd'],
            'Entry_point': content['Config']['Entrypoint'],
            'Memory': content['HostConfig']['Memory'],
            'Memory_swap': content['HostConfig']['MemorySwap'],
            'IP': content.get('NetworkSettings')['IPAddress']
        }
        exposed_port = content['HostConfig']['PortBindings'].keys()
        port_binding = content['HostConfig']['PortBindings'].values()
        port_map = []
        for index in range(0, len(port_binding)):
            port = exposed_port[index] + ':' + port_binding[index][0]['HostPort']
            port_map.append(port)
        content_json['port_map'] = port_map
        content = {
            'status': True,
            'content': content_json
        }
        return content
