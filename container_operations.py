from docker_server import DockerServer
from constants import DockerEndPoint, ContainerOperation
from utils import _multiplexed_buffer_helper


class ContainerOperations(DockerServer):

    def __init__(self, host, tls_verify=False, cert=None, key=None, ca=False):
        super(ContainerOperations, self).__init__(host, tls_verify, cert, key, ca)

    def list_container(self, all=False, limit=None, since=None, before=None, size=False, filters=None):
        """
        :param bool all: List all the containers in a host.(Default False) 
        :param int limit: Show 'limit' last created containers, include non-running ones(Default is None)
        :param str since: Show containers created 'since' Id, include non-running ones(Default is None)
        :param str before: Show containers created 'before' Id, include non-running ones(Default is None)
        :param bool size: Show container sizes. (Default is False)
        :param dict filters: Available filters
                                1. exited=<int>; -- containers with exit code of <int> 
                                2. status=(restarting|running|paused|exited)
                                3. label=key or label="key=value" of a container label

        List all the containers in docker host.

        .. code-block:: python

            docker.list_container()

        Output

        .. code-block:: json            

            {'content': [{u'Command': u'/bin/sh -c /usr/bin/pidgin',
               u'Created': 1454476022,
               u'HostConfig': {u'NetworkMode': u'default'},
               u'Id': u'a7da5a495448085ce1fc57deae89b444ffb56d35c1b727750c988c6ca226e771',
               u'Image': u'pidgin:latest',
               u'ImageID': u'4bd0d7652bf3c89f191b5deae84e891e4f3e76d60bf2ed4358a080ed41a22c3d',
               u'Labels': {},
               u'Names': [u'/pidgin'],
               u'Ports': [],
               u'Status': u'Restarting (1) 30 hours ago'}],
             'status': True}

        """

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
        """ 
        :param str container_id: Container id/name
        :param bool raw_json: Get the filtered details of container(Default is False)
        
        Return low-level information on the container id.

        .. code-block:: python

            docker.inspect_container('a7da5a495448')
        
        Output

        .. code-block:: json

            {'content': {u'AppArmorProfile': u'',
              u'Args': [u'-c', u'/usr/bin/pidgin'],
              u'Config': {u'AttachStderr': False,
               u'AttachStdin': False,
               u'AttachStdout': False,
               u'Cmd': [u'/bin/sh', u'-c', u'/usr/bin/pidgin'],
               u'Domainname': u'',
               u'Entrypoint': None,
               u'Env': [u'DISPLAY=:0', u'NSS_SSL_CBC_RANDOM_IV=0'],
               u'Hostname': u'a7da5a495448',
               u'Image': u'pidgin:latest',
               u'Labels': {},
               u'OnBuild': None,
               u'OpenStdin': False,
               u'StdinOnce': False,
               u'StopSignal': u'SIGTERM',
               u'Tty': False,
               u'User': u'',
               u'Volumes': None,
               u'WorkingDir': u''},
              ...
              }

        """
        response = self._get(DockerEndPoint.INSPECT_CONTAINER.format(container_id))
        if raw_json and response['status']:
            return self._prepare_container_info_json(response['content'])
        return response

    def create_container_from_config(self, configuration, name=None):
        """
        :param dict configuration: Configuration of the container.
        :param str name: Name of the container(Default is None)

        Create a container from an image.



        """
        headers = {'content-type': 'application/json'}
        return self._post(''.join([DockerEndPoint.CREATE_CONTAINER, '?name=' + name if name else '']), configuration, headers)

    def start_container(self, container_id):
        """
        :param str container_id: Container Id to start.

        Start the container id.

        .. code-block:: python

            docker.start_container('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.START))

    def stop_container(self, container_id):
        """
        :param str container_id: Container Id to stop.

        Stop the container id.

        .. code-block:: python

            docker.stop_container('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.STOP))

    def restart_container(self, container_id):
        """
        :param str container_id: Container Id to restart.

        Restart the container id.

        .. code-block:: python

            docker.restart_container('0bd62601d47c')
            
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.RESTART))

    def pause_container(self, container_id):
        """
        :param str container_id: Container Id to pause.

        Pause the container id.

        .. code-block:: python

            docker.pause_container('0bd62601d47c')

        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.PAUSE))

    def unpause_container(self, container_id):
        """
        :param str container_id: Container Id to unpause.

        Unpause the container id.

        .. code-block:: python

            docker.unpause_container('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.UNPAUSE))

    def rename_container(self, container_id, name):
        """
        :param str container_id: Container Id to rename.
        :param str name: New name for the container

        Rename the container id.

        .. code-block:: python

            docker.rename_container('0bd62601d47c', 'new_name')
        
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        return self._post(DockerEndPoint.CONTAINER_OPERATION.format(container_id, ContainerOperation.RENAME), {'name': name})

    def remove_container(self, container_id, force=False, volume=False):
        """
        :param str container_id: Container Id to remove.
        :param bool force: Forcefully remove container(Default is False)
        :param bool volume: Remove volume associated to the container(Default is False)

        Remove the container id.

        .. code-block:: python

            docker.remove_container('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': '', 'status': True}

        """
        params = {
            'force': force,
            'v': volume
        }
        return self._delete(DockerEndPoint.REMOVE_CONTAINER.format(container_id), params)

    def commit_container(self, container_id, image_name=None, tag=None, comment=None, author=None):
        """
        :param str container_id: Container Id to commit.
        :param str image_name: Repository name
        :param str tag: Tag
        :param str comment: Comment
        :param str author: Author
        
        Save the container as new image.

        .. code-block:: python

            docker.commit_container('cb8c119188c9', 'new_image', 'latest', 'Created by marlabs', author='user@marlabs.com')
        
        Output

        .. code-block:: json

            {'content': {u'Id': u'5a33144e868819349f1df4550ebdfd17661589efbf3f727f287f25de40526ad0'}, 'status': True}


        """
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
        """
        :param str container_id: Container Id to commit.
        
        Get container statitics of running container.

        .. code-block:: python

            r = docker.get_container_statics('cb8c119188c9')
            r['content'].next()

        Output

        .. code-block:: json
            
            '{"read":"2016-02-09T14:31:34.283155198+05:30","precpu_stats":{"cpu_usage":{"total_usage":0,"percpu_usage":null,"usage_in_kernelmode":0,"usage_in_usermode":0},"system_cpu_usage":0,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"cpu_stats":{"cpu_usage":{"total_usage":39187676,"percpu_usage":[3032123,12531305,4135257,19488991],"usage_in_kernelmode":0,"usage_in_usermode":20000000},"system_cpu_usage":1317876330000000,"throttling_data":{"periods":0,"throttled_periods":0,"throttled_time":0}},"memory_stats":{"usage":1024000,"max_usage":6897664,"stats":{"active_anon":266240,"active_file":233472,"cache":524288,"hierarchical_memory_limit":18446744073709551615,"inactive_anon":270336,"inactive_file":253952,"mapped_file":45056,"pgfault":3216,"pgmajfault":8,"pgpgin":2322,"pgpgout":2072,"rss":499712,"rss_huge":0,"total_active_anon":266240,"total_active_file":233472,"total_cache":524288,"total_inactive_anon":270336,"total_inactive_file":253952,"total_mapped_file":45056,"total_pgfault":3216,"total_pgmajfault":8,"total_pgpgin":2322,"total_pgpgout":2072,"total_rss":499712,"total_rss_huge":0,"total_unevictable":0,"total_writeback":0,"unevictable":0,"writeback":0},"failcnt":0,"limit":8187768832},"blkio_stats":{"io_service_bytes_recursive":[{"major":8,"minor":0,"op":"Read","value":487424},{"major":8,"minor":0,"op":"Write","value":0},{"major":8,"minor":0,"op":"Sync","value":0},{"major":8,"minor":0,"op":"Async","value":487424},{"major":8,"minor":0,"op":"Total","value":487424}],"io_serviced_recursive":[{"major":8,"minor":0,"op":"Read","value":19},{"major":8,"minor":0,"op":"Write","value":0},{"major":8,"minor":0,"op":"Sync","value":0},{"major":8,"minor":0,"op":"Async","value":19},{"major":8,"minor":0,"op":"Total","value":19}],"io_queue_recursive":[],"io_service_time_recursive":[],"io_wait_time_recursive":[],"io_merged_recursive":[],"io_time_recursive":[],"sectors_recursive":[]},"networks":{"eth0":{"rx_bytes":5380,"rx_packets":36,"rx_errors":0,"rx_dropped":0,"tx_bytes":648,"tx_packets":8,"tx_errors":0,"tx_dropped":0}}}'

        """
        return self._get(DockerEndPoint.CONTAINER_STATS.format(container_id), stream=True)

    def get_container_logs(self, container_id, std_out=True, std_err=True, date_time=0, time_stamp=False, count='all'):
        """

        :param str container_id: Container Id
        :param bool std_out: Get stdout logs(Default is True)
        :param bool std_err: Get std_err logs(Default is True)
        :param int date_time: UNIX timestamp to filter logs.(Default 0)
        :param bool time_stamp: print timestamp for every log line.(Default is False)
        :param int count: Specified number of lines at the end of logs(Default is all)

        Get container logs.

        .. code-block:: python
        
            docker.get_container_logs('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': 'error: missing MYSQL_PORT_3306_TCP environment variable. Did you forget to --link some_mysql_container:mysql ?', 'status': True}

        """
        d = {'stdout': std_out, 'stderr': std_err, 'since': date_time, 'timestamps': time_stamp, 'tail': count}
        params = '&'.join(['{}={}'.format(k, v) for k, v in d.iteritems()])
        end_url = '?'.join([DockerEndPoint.CONTAINER_LOGS.format(container_id), params])
        response = self._get(end_url)

        response['content'] = ''.join([x for x in _multiplexed_buffer_helper(response['content'])])
        return response

    def list_container_process(self, container_id, ps_args=None):
        """
        :param str container_id: Container Id.
        :param str ps_args: ps arguments to use(eg: aux)

        List the process inside a container.

        .. code-block:: python

            docker.list_container_process('0bd62601d47c')
        
        Output

        .. code-block:: json

            {'content': {u'Processes': [[u'root',
                u'26764',
                u'1919',
                u'0',
                u'12:54',
                u'pts/19',
                u'00:00:00',
                u'/bin/bash']],
              u'Titles': [u'UID',
               u'PID',
               u'PPID',
               u'C',
               u'STIME',
               u'TTY',
               u'TIME',
               u'CMD']},
             'status': True}


        """
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
