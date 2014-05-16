#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
  name='pyanx',
  author='Petter Bjelland',
  version='0.1',
  author_email='petter.bjelland@gmail.com',
  description='API for generating Analyst\'s Notebook (ANB) ANX files.',
  license='Apache2',    
  scripts=[],
  packages=['pyanx'],
  install_requires=[
    'networkx',
    'matplotlib',
  ]
)
