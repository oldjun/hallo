#!/usr/bin/env python
from setuptools import setup, find_packages

version = '0.0.9'

with open("./README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="Hallo",
    version=version,
    url='https://github.com/oldjun/hallo',
    author='JP Chen',
    author_email='oldjun@sina.com',
    description='web mvc framework for python',
    long_description=readme,
    long_description_content_type='text/markdown',
    python_requires=">=3.6",
    install_requires=[
    ],
    license="MIT",
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Database',
    ],
    entry_points={
        'console_scripts': ['hallo=hallo.__main__:main'],
    },
    include_package_data=True
)
