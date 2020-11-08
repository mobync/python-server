import pathlib
from setuptools import setup
import os
import re

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

cwd = os.path.sep.join(__file__.split(os.path.sep)[:-1])


def get_module_info():
    """
    reads the basic __stat__ strings from our module's init
    """

    stat_regex = re.compile(r"^__(.+)__ = '(.+)'$")
    result = {}

    with open(os.path.join(cwd, 'mobync', '__init__.py')) as init_file:
        for line in init_file.readlines():
            line_match = stat_regex.match(line)

            if line_match:
                keyword, value = line_match.groups()
                result[keyword] = value

    return result


def get_install_requirements():
    """
    reads the requirements strings from our module's requirements.txt
    """

    result = list()

    with open(os.path.join(cwd, 'mobync', 'requirements.txt')) as requirements_file:
        for line in requirements_file.readlines():
            result.append(line)

    return result


module_info = get_module_info()

setup(
    name="mobync",
    version=module_info['version'],
    description="The Library for online-offline synchronization",
    long_description=README,
    long_description_content_type="text/markdown",
    license=module_info['license'],
    author=module_info['author'],
    author_email=module_info['contact'],
    url=module_info['url'],
    packages=["mobync"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    install_requires=get_install_requirements(),
)
