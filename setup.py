#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="baseball-stats-mcp",
    version="1.0.1",
    author="Arin Gadre",
    author_email="aringadre76@gmail.com",
    description="The most comprehensive baseball analytics MCP server with 32 advanced tools",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/aringadre76/baseball-stats-mcp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "baseball-stats-mcp=baseball_stats_mcp.server:main",
        ],
    },
    keywords="baseball, mcp, analytics, statcast, sabermetrics, mlb, sports, statistics",
    project_urls={
        "Homepage": "https://github.com/aringadre76/baseball-stats-mcp",
        "Repository": "https://github.com/aringadre76/baseball-stats-mcp",
        "Source": "https://github.com/aringadre76/baseball-stats-mcp",
        "Bug Reports": "https://github.com/aringadre76/baseball-stats-mcp/issues",
        "Issues": "https://github.com/aringadre76/baseball-stats-mcp/issues",
        "Documentation": "https://github.com/aringadre76/baseball-stats-mcp/blob/main/docs/",
    },
    include_package_data=True,
    zip_safe=False,
)
