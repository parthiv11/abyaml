from setuptools import setup, find_packages

setup(
    name="abyaml",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
        "requests",
        "argparse",
    ],
    entry_points={
        "console_scripts": [
            "abyaml=abyaml.cli:main",  
        ],
    },
)
