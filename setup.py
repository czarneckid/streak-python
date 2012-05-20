import streak
import os

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

requirements = map(str.strip, open('requirements.txt').readlines())

setup(
  name = 'streak',
  version = streak.__version__,
  author = 'David Czarnecki',
  author_email = "me@davidczarnecki.com",
  packages = ['streak'],
  install_requires = requirements,
  url = 'https://github.com/czarneckid/streak-py',
  license = "LICENSE",
  description = 'Library for calculating win/loss streaks using Redis as a backend',
  long_description = open('README.md').read(),
  keywords = ['python', 'redis', 'win/loss'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'License :: OSI Approved :: MIT License',
    "Intended Audience :: Developers",
    "Operating System :: POSIX",
    "Topic :: Communications",
    "Topic :: Software Development :: Libraries :: Python Modules",
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Software Development :: Libraries'
  ]
)
