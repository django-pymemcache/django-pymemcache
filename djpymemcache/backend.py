try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core.cache.backends.memcached import BaseMemcachedCache


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
        import pymemcache.client
        if isinstance(server, basestring):
            server = server.split(';')
        server = server[0]  # Only support one server for now.
        super(PyMemcacheCache, self).__init__(server, params,
                                              library=pymemcache.client,
                                              value_not_found_exception=ValueError)

    @property
    def _cache(self):
        # pymemcached uses cache options as kwargs to the __init__ method.
        if getattr(self, '_client', None) is None:
            options = {
                'serializer': serialize_pickle,
                'deserializer': deserialize_pickle,
            }
            options.update(**self._options)
            host, port = self._servers[0].split(':')
            server = (host, int(port))
            self._client = self._lib.Client(server, **options)
        return self._client
