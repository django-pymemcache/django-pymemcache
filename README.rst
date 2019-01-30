django-pymemcache
=================

django-pymemcache is a Django cache backend that uses Pinterest's
pymemcache_ library as the backend.

Installation
------------

::

    pip install django-pymemcache

Usage
-----

Simply use it as any other Cache backend, e.g.::

    CACHES = {
        'default': {
            'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
            'LOCATION': [
               '127.0.0.1:11211',
            ],
        },
    }

Issues
------

    https://github.com/django-pymemcache/django-pymemcache/issues

.. _pymemcache: https://github.com/pinterest/pymemcache
