#!/usr/bin/env python

from setuptools import find_packages, setup

from djpymemcache import __version__

requirements = [
    'Django>=1.11',
    'pymemcache',
]


setup(
    name='django-pymemcache',
    version=__version__,
    description="Django cache backend based on Pinterest's pymemcache client.",
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='me@jamessocol.com',
    url='https://github.com/django-pymemcache/django-pymemcache',
    license='Apache Software License 2.0',
    packages=find_packages(exclude=('tests')),
    install_requires=requirements,
    test_suite='runtests.runtests',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
