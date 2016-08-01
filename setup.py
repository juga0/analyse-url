#!/usr/bin/env python

#   This file is part of analyse_url, a set of scripts to
#   use different tor guards depending on the network we connect to.
#
#   Copyright (C) 2016 juga (juga at riseup dot net)
#
#   analyse_url is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License Version 3 of the
#   License, or (at your option) any later version.
#
#   analyse_url is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with analyse_url.  If not, see <http://www.gnu.org/licenses/>.
#


# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path
from pip.req import parse_requirements
from analyse_url import __version__, __author__, __contact__

here = path.abspath(path.dirname(__file__))
install_reqs = parse_requirements(path.join(here, 'requirements.txt'),
                                  session=False)
reqs = [str(ir.req) for ir in install_reqs]

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='analyse_url',
    version=__version__,
    description='analyse_url...',
    long_description=long_description,
    #url='https://github.com/openintegrity/analyse-url',
    url='https://meta.openintegrity.org/agents/analyse-url',
    author='__author__',
    author_email=__contact__,
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        "Environment :: Console",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        "Natural Language :: English",
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    keywords='agents analyse page tos',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    #   py_modules=["my_module"],
    # install_requires=reqs,
    install_requires=['nameko==2.3.1'],
    dependency_links=['https://meta.openintegrity.org/agents/agents-common-code.git#egg=agents-common'],
    extras_require={
        'dev': ['ipython'],
        'test': ['coverage'],
        'test': ['pytest'],
        'test': ['sphinx'],
    },
    # package_data={
    #     'analyse_url': ['package_data.dat'],
    # },
    # data_files=[('my_data', ['data/data_file'])],
    # entry_points={
    #     'console_scripts': [
    #         'analyse_url=analyse_url:main',
    #     ],
    # },
)
