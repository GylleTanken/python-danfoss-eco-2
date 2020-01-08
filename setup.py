#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from setuptools import setup, find_packages
import sys
import warnings

dynamic_requires = []

version = '0.1.1'

setup(
    name='DanfossEco2',
    version=version,
    url='https://github.com/GylleTanken/python-danfoss-eco-2',
    packages=find_packages(),
    install_requires=['bluepy==1.3.0', 'xxtea==1.3.0'],
    scripts=[],
    description='Python API for controlling Danfoss Eco 2',
    classifiers=[
        'Development Status :: 1 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    include_package_data=True,
    zip_safe=False,
)
