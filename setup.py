"""Setup for transcript transcriber."""
from setuptools import setup


extra_packages = {
    'testing': ['pytest']
}


setup(
    name='scrapers',
    description='Contains various scrapers for different websites'
                'and a script that threw objects into MongoDB.',
    version=0.1,
    author='Kurt Maurer',
    author_email='kurtrm@gmail.com',
    install_requires=['bs4', 'selenium'],
    extras_require=extra_packages
)
