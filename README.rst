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

.. note::

    The backend currently only supports connecting to one server.

Issues
------

    https://github.com/jsocol/django-pymemcache/issues


.. _pymemcache: https://github.com/pinterest/pymemcache
