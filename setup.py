#! /usr/bin/env python
from distutils.core import setup

setup(name='plttools',
      version='1.0',
      description='Small tools for matplotlib',
      author='Jan Eike von Seggern',
      author_email='eikevons@yahoo.de',
      packages=['plttools'],
      requires=['numpy', 'matplotlib']
      )
