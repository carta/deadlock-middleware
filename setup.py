import os
import sys

from setuptools import setup
import setuptools.command.test

try:
    long_description = open("README.md").read()
except IOError:
    long_description = ""


# -*- Command: setup.py test -*-
class pytest(setuptools.command.test.test):
    user_options = [("pytest-args=", "a", "Arguments to pass to py.test")]

    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)
        self.pytest_args = []

    def run_tests(self):
        import pytest as _pytest

        sys.exit(_pytest.main(self.pytest_args))


def _strip_comments(l):
    return l.split("#", 1)[0].strip()


def _pip_requirement(req):
    if req.startswith("-r "):
        _, path = req.split()
        return reqs(*path.split("/"))
    return [req]


def _reqs(*f):
    return [
        _pip_requirement(r)
        for r in (
            _strip_comments(l)
            for l in open(os.path.join(os.getcwd(), "requirements", *f)).readlines()
        )
        if r
    ]


def reqs(*f):
    """Parse requirement file.
    Example:
        reqs('default.txt')          # requirements/default.txt
        reqs('extras', 'redis.txt')  # requirements/extras/redis.txt
    Returns:
        List[str]: list of requirements specified in the file.
    """
    return [req for subreq in _reqs(*f) for req in subreq]


setup(
    name="deadlock-middleware",
    version="0.0.2",
    description="A django middleware to automatically retry requests in the case of a deadlock.",
    license="Apache Software License",
    author="Carson Crane",
    author_email="carson.crane@carta.com",
    packages=["deadlock_middleware"],
    install_requires=reqs("release.txt"),
    tests_require=reqs("dev.txt"),
    cmdclass={"test": pytest},
    long_description=long_description,
    include_package_data=False,
    url="https://github.com/carta/%s" % "deadlock-middleware",
    classifiers=[
        "Development Status :: 0 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5.3",
        "OSI Approved :: Apache Software License",
    ],
)
