from threading import local

import pymemcache
from django.core.cache.backends.memcached import BaseMemcachedCache


class PyMemcacheCache(BaseMemcachedCache):
    """An implementation of a cache binding using pymemcache."""

    def __init__(self, server, params):
        self._local = local()
        super(PyMemcacheCache, self).__init__(server, params,
                                              library=pymemcache,
                                              value_not_found_exception=KeyError)

    @property
    def _cache(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client

        # pymemcached uses cache options as kwargs to the __init__ method.
        options = {
            'serializer': pymemcache.serde.python_memcache_serializer,
            'deserializer': pymemcache.serde.python_memcache_deserializer,
        }
        if self._options:
            options.update(**self._options)
        host, port = self._servers[0].split(':')
        server = (host, int(port))
        self._local.client = self._lib.Client(server, **options)
        return self._local.client
