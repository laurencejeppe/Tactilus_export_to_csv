# -*- coding: utf-8 -*-
"""
Copyright: Joshua Steer 2020, Joshua.Steer@soton.ac.uk
"""

from setuptools import setup, find_packages
from os import path, walk


def readme():
    with open('README.md') as f:
        return f.read()

def requirements():
    with open('requirements.txt') as f:
        return f.read().split('\n')


setup(name='tactilexp',
      version='0.1.0',
      description=('Package for converting Tactilus export '
                   'to CSV files'),
      long_description=readme(),
      author='Laurence Russell',
      author_email='l.j.russell@soton.ac.uk',
      license='MIT',
      include_package_data=True,
      packages=find_packages(),
      python_requires='>=3.5',  # Your supported Python ranges
      install_requires=requirements(),
      zip_safe=False,)