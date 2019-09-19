#!/usr/bin/env python

import pathlib

from setuptools import find_packages, setup

version = __import__('aioworkers_prometheus').__version__

requirements = [
    'aioworkers>=0.12.0',
]

readme = pathlib.Path('README.rst').read_text()


setup(
    name='aioworkers-prometheus',
    version=version,
    description='aioworkers prometheus integration',
    long_description=readme,
    author='Alexander Malev',
    author_email='aamalev@gmail.com',
    url='https://github.com/aioworkers/aioworkers-prometheus',
    packages=[
        i for i in find_packages()
        if i.startswith('aioworkers_prometheus')
    ],
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    keywords='aioworkers',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='tests',
)
