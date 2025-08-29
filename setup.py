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
    version="1.0.0",
    author="Your Name",  # Update this
    author_email="your.email@example.com",  # Update this
    description="The most comprehensive baseball analytics MCP server with 32 advanced tools",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/baseball-stats-mcp",  # Update this
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
        "Bug Reports": "https://github.com/yourusername/baseball-stats-mcp/issues",  # Update this
        "Source": "https://github.com/yourusername/baseball-stats-mcp",  # Update this
        "Documentation": "https://github.com/yourusername/baseball-stats-mcp/blob/main/docs/",  # Update this
    },
    include_package_data=True,
    zip_safe=False,
)
