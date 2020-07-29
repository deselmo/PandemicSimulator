from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
name = 'pandemic_analyzer'

setup(
    name=name,
    version='1.0.0',
    install_requires=["matplotlib"],
    entry_points={
        'console_scripts': [
            '{}={}.__main__:main'.format(name, name),
        ],
    }
)
