from threading import local

from django.core.cache.backends.base import InvalidCacheBackendError
from django.core.cache.backends.memcached import BaseMemcachedCache

try:
    from . import client
except ImportError:
    raise InvalidCacheBackendError('Could not import pymemcache.')


class PyMemcacheCache(BaseMemcachedCache):
    """An implementation of a cache binding using pymemcache."""

    def __init__(self, server, params):
        self._local = local()
        super(PyMemcacheCache, self).__init__(
            server,
            params,
            library=client,
            value_not_found_exception=KeyError,
        )

    @property
    def _cache(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client

        client = self._lib.Client(self._servers, **self._options)
        if self._options:
            client.behaviors = self._options

        self._local.client = client

        return client
