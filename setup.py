import setuptools
from setuptools.command.install import install
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="groundmag",
    version="0.0.2",
    author="Matthew Knight James",
    author_email="mattkjames7@gmail.com",
    description="A small package designed for reading ground magnetometer data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mattkjames7/groundmag",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
    ],
    install_requires=[
		'numpy',
		'matplotlib',
		'DateTimeTools',
		'aacgmv2',
		'pyIGRF',
		'wavespec>=0.0.4',
		'RecarrayTools',
		'PyFileIO',
	],
	include_package_data=True,
)



