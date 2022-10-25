#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='python-mcp3425',
      version='1.0.1',
      description='A Python3 library for the Microchip MS3425 single channel ADC',
      author='Mantis Sub',
      url='https://www.mantis-sub.com/',
      install_requires=[
          'smbus2',
      ],
      packages=find_packages()
      )
