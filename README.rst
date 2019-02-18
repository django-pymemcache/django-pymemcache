django-pymemcache
=================

.. image:: https://travis-ci.org/django-pymemcache/django-pymemcache.svg?branch=master
   :target: https://travis-ci.org/django-pymemcache/django-pymemcache
.. image:: https://codecov.io/gh/django-pymemcache/django-pymemcache/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/django-pymemcache/django-pymemcache
.. image:: https://img.shields.io/pypi/v/django-pymemcache.svg?style=flat
   :target: https://pypi.org/project/django-pymemcache/
.. image:: https://img.shields.io/pypi/djversions/django-pymemcache.svg?style=flat
.. image:: https://img.shields.io/pypi/pyversions/django-pymemcache.svg?style=flat

django-pymemcache is a Django cache backend that uses Pinterest's
pymemcache_ library as the backend.

Installation
------------

::

    pip install django-pymemcache

Usage
-----

Simply use it as any other `Cache backend <https://docs.djangoproject.com/en/stable/topics/cache/>`_, e.g.

.. code-block:: python

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
