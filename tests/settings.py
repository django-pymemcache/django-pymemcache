SECRET_KEY = 's3cr3t'
INSTALLED_APPS = [
    'tests',
]

DATABASES = {
    'default': {
        'NAME': ':memory:',
        'ENGINE': 'django.db.backends.sqlite3',
    },
}

CACHES = {
    'default': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    },
    'v2': {
        'BACKEND': 'djpymemcache.backend.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
        'VERSION': 2,
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
