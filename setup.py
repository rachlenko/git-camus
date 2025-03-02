#!/usr/bin/env python3
"""Setup script for git-camus."""

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="git-camus",
    version="0.1.0",
    author="Evgeny Rachlenko",
    author_email="evgeny.rachlenko@gmail.com",
    description="Craft Git Commit Messages with Existential Flair",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rachlenko/git-camus",
    packages=setuptools.find_packages(),
    py_modules=["git_camus"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=["click>=8.0.0", "httpx>=0.24.0"],
    entry_points={"console_scripts": ["git-camus=git_camus:main"]},
)
