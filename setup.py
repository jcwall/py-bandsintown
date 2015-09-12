#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as req:
    requirements = req.read().splitlines()

with open('README.md') as readme:
    long_description = readme.read()

setup(name='py-bandsintown',
      version='0.1.0',
      description='Unofficial Python Wrapper for BandsInTown API 1.0',
      long_description=long_description,
      url='https://github.com/papernotes/py-bandsintown',
      author='Jonathan (papernotes)',
      packages=find_packages(),
      license='MIT',
      keywords='bandsintown api wrapper',
      install_requires=requirements,
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ]
)

