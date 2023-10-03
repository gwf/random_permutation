
"""
This setup file is used to package the random_permutation module.
The module is used for efficiently generating very large random permutations.
"""

from setuptools import setup, find_packages

setup(
  name='random_permutation',
  version='0.1.0',
  author='Gary William Flake',
  author_email='gary@flake.org',
  description=
  'A module for efficiently generating very large random permutations',
  packages=find_packages(
    include=['random_permutation', 'random_permutation.*']),
  install_requires=[],
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
  ],
)

