#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

try:
    import setuptools
    setup = setuptools.setup
except ImportError:
    setuptools = None
    from distutils.core import setup

def read(*names, **kwargs):
    return io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='ufile',
    version=find_version("ufile/__init__.py"),
    description='UCloud UFile Python SDK',
    author_email='leo.li@ucloud.cn',
    url="https://github.com/ucloud/ufile-sdk-python",
    platforms='any',
    packages=['ufile'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    install_requires=['requests'],

)
