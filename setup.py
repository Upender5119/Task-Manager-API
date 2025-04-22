'''
SetUp src package Globally
'''

from setuptools import find_namespace_packages, find_packages, setup

setup(name='External project',
      version='1.0',
      packages=find_packages(where="src"),
      package_dir={'': 'src'},
      zip_safe=False)
