#! /usr/bin/env python
from distutils.core import setup

setup(name='plttools',
      version='0.0.1',
      description='Tools to read and process CCD images',
      author='Jan Eike von Seggern',
      author_email='jan.eike.von.seggern@desy.de',
      packages=['plttools'],
      requires=['numpy', 'matplotlib']
      )
