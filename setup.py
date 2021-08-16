#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
===============================
HtmlTestRunner
===============================


.. image:: https://img.shields.io/pypi/v/glacier.svg
        :target: https://pypi.python.org/pypi/glacier
.. image:: https://img.shields.io/travis/alperozaydin/glacier.svg
        :target: https://travis-ci.org/alperozaydin/glacier

Contains AWS Glacier sample codes


Links:
---------
* `Github <https://github.com/alperozaydin/glacier>`_
"""

from setuptools import setup, find_packages

requirements = [
    "Click>=6.0",
]

setup_requirements = []

test_requirements = []

setup(
    author="Alper Ozaydin",
    author_email="alperozaydinn@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    description="Contains AWS Glacier sample codes",
    entry_points={
        "console_scripts": [
            "glacier=glacier.cli:main",
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=__doc__,
    include_package_data=True,
    keywords="glacier",
    name="glacier",
    packages=find_packages(include=["glacier"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/alperozaydin/glacier",
    version="0.1.0",
    zip_safe=False,
)
