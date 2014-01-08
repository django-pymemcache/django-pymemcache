try:
    import cPickle as pickle
except ImportError:
    import pickle
from threading import local

from django.core.cache.backends.memcached import BaseMemcachedCache

from . import client


def serialize_pickle(key, value):
    if isinstance(value, basestring):
        return value, 1
    return pickle.dumps(value), 2

def deserialize_pickle(key, value, flags):
    if flags == 1:
        return value
    if flags == 2:
        return pickle.loads(value)
    raise Exception('Unknown flags for value: {1}'.format(flags))


class PyMemcacheCache(BaseMemcachedCache):
    """An implementation of a cache binding using pymemcache."""

    def __init__(self, server, params):
        self._local = local()
        super(PyMemcacheCache, self).__init__(server, params,
                                              library=client,
                                              value_not_found_exception=ValueError)

    @property
    def _cache(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client

        # pymemcached uses cache options as kwargs to the __init__ method.
        options = {
            'serializer': serialize_pickle,
            'deserializer': deserialize_pickle,
        }
        if self._options:
            options.update(**self._options)
        host, port = self._servers[0].split(':')
        server = (host, int(port))
        self._local.client = self._lib.Client(server, **options)
        return self._local.client
