#!/usr/bin/env python3
import os
from setuptools import setup, find_packages
from typing import List


import os
import setuptools


def _read_reqs(requirements_filename: str = "requirements.txt") -> List:
    full_path = os.path.join(os.path.dirname(__file__), requirements_filename)
    requirements = list()
    with open(full_path) as fp:
        for line in fp:
            line = line.split("#", 1)[0].strip()
            if len(line) > 0:
                requirements.append(line)
    return requirements


_REQUIREMENTS_TXT = _read_reqs("requirements.txt")
_INSTALL_REQUIRES = [line for line in _REQUIREMENTS_TXT if "://" not in line]


_SETUP_ARGS = {
    "data_files": [(".", ["requirements.txt"])],
    "packages": find_packages(),
    "include_package_data": True,
}

setup(name="mctchess", version="0.0.1", packages=find_packages())
