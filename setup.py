#!/usr/bin/env python3
"""
Setup script for StormRunner distribution
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="stormrunner",
    version="1.0.0",
    author="StormRunner Studios",
    author_email="contact@stormrunner.com",
    description="A thrilling 3D-style adventure game with avatar customization and dynamic weather",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stormrunner/stormrunner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Games/Entertainment :: Arcade",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "stormrunner=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.yml"],
    },
    keywords="game, adventure, 3d, weather, avatar, pygame",
    project_urls={
        "Bug Reports": "https://github.com/stormrunner/stormrunner/issues",
        "Source": "https://github.com/stormrunner/stormrunner",
        "Documentation": "https://github.com/stormrunner/stormrunner/wiki",
    },
)