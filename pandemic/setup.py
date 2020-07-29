from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
name = 'pandemic'

setup(
    name=name,
    version='1.0.0',
    install_requires=["numpy", "tk"],
    entry_points={
        'console_scripts': [
            '{}={}.cli:main'.format(name, name),
            '{}-cli={}.cli:main'.format(name, name),
            '{}-gui={}.gui:main'.format(name, name),
        ],
    }
)
