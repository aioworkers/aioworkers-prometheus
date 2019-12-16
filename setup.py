import re
from pathlib import Path

from setuptools import find_packages, setup

requirements = [
    'aioworkers>=0.12.0',
    'prometheus-client',
]

pkg = 'aioworkers_prometheus'


def read(f):
    path = Path(__file__).parent / f
    if not path.exists():
        return ''
    return path.read_text(encoding='latin1').strip()


def get_version():
    text = read(pkg + '/version.py')
    if not text:
        text = read(pkg + '/__init__.py')
    try:
        return re.findall(r"__version__ = '([^']+)'$", text, re.M)[0]
    except IndexError:
        raise RuntimeError('Unable to determine version.')


setup(
    name='aioworkers-prometheus',
    version=get_version(),
    description='aioworkers prometheus integration',
    long_description=Path('README.rst').read_text(),
    author='Alexander Malev',
    author_email='aamalev@gmail.com',
    url='https://github.com/aioworkers/aioworkers-prometheus',
    packages=find_packages(include=[pkg, pkg + '.*']),
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    keywords='aioworkers prometheus',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
