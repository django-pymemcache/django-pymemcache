from pymemcache.client.hash import HashClient
from pymemcache.serde import (
    python_memcache_deserializer,
    python_memcache_serializer,
)


def _split_host_and_port(servers):
    """Convert python-memcached based server strings to pymemcache's one.

    - python-memcached: ['127.0.0.1:11211', ...] or ['127.0.0.1', ...]
    - pymemcache: [('127.0.0.1', 11211), ...]
    """
    _host_and_port_list = []
    for server in servers:
        connection_info = server.split(':')
        if len(connection_info) == 1:
            _host_and_port_list.append(
                (connection_info[0], 11211))
        elif len(connection_info) == 2:
            _host_and_port_list.append(
                (connection_info[0], int(connection_info[1])))
    return _host_and_port_list


class Client(HashClient):
    """pymemcache client.

    Customize pymemcache behavior as python-memcached (default backend)'s one.
    """

    def __init__(self, servers, *args, **kwargs):
        kwargs.setdefault('serializer', python_memcache_serializer)
        kwargs.setdefault('deserializer', python_memcache_deserializer)

        super(Client, self).__init__(
            _split_host_and_port(servers),
            *args,
            **kwargs
        )

    def disconnect_all(self):
        for client in self.clients.values():
            client.close()

    def get_many(self, keys, gets=False, *args, **kwargs):
        # pymemcache's HashClient may returns {'key': False}
        end = super(Client, self).get_many(keys, gets, *args, **kwargs)

        return {key: end.get(key) for key in end if end.get(key)}

    get_multi = get_many
