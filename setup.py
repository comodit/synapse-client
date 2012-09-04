from platform import python_version
from setuptools import setup, find_packages


major, minor, micro = python_version().split('.')

if major != '2' or minor not in ['6', '7']:
    raise Exception('unsupported version of python')

syncli_version = "Undefined"
try:
    import syncli.version as version_mod
    if version_mod.VERSION:
        syncli_version = version_mod.VERSION
except (ImportError, AttributeError):
    pass

requires = [
    'pika == 0.9.5-1',
]

dependency_links = [
    'http://github.com/raphdg/pika/tarball/ssl#egg=pika-0.9.5-1'
]

setup(
    name='synapse-client',
    version=syncli_version,
    description='Client for synapse',
    author='Raphael De Giusti, Sandro Munda',
    author_email='raphael.degiusti@gmail.com',
    url='https://github.com/comodit/synapse-client',
    license='MIT License',
    packages=find_packages(),
    scripts=['bin/synapse-client'],
    data_files=[('/etc/synapse-client/', ['conf/synapse-client.conf',
                                          'conf/synapse-client-logger.conf']),
                ('/etc/bash_completion.d/', ['scripts/synapse-client'])
    ],
    include_package_data=True,
    dependency_links=dependency_links,
    classifiers=[
        'License :: License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Topic :: Content Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
    ],
    install_requires=requires,
)
