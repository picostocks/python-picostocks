#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = ["requests==2.18.4", "ed25519==1.4"]

setup(
    author="picostocks",
    author_email='',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    description=("This is an official Python wrapper for the Picostocks "
                 "exchange REST API."),
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    include_package_data=True,
    keywords='pico picostocks exchange rest api bitcoin ehtereum btc eth',
    name='python-picostocks-api',
    packages=['picostocks'],
    url='https://github.com/picostocks/python-picostocks-api',
    version='0.1.1',
)