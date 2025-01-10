"""Setup configuration for hunter-sdk package."""

from setuptools import setup, find_packages

setup(
    name="hunter-sdk",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
) 