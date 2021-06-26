#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name="gainloss",
    version="0.1.0",
    description="Trading PnL Calculation",
    author="evalbuena",
    author_email="enrique.millanvalbuena@gmail.com",
    url="https://github.com/KikeM/gainloss",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pandas", "tabulate", "click"],
    entry_points={"console_scripts": ["pnl=gainloss.cli:compute_pnl"]},
)
