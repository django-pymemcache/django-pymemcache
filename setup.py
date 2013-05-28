from setuptools import setup, find_packages

from djpymemcache import __version__


setup(
    name='djpymemcache',
    version=__version__,
    description="Django cache backend based on Pinterest's pymemcache client.",
    long_description=open('README.rst').read(),
    author='James Socol',
    author_email='me@jamessocol.com',
    url='https://github.com/jsocol/django-pymemcache',
    license='Apache Software License 2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
