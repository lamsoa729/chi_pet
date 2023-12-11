#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyyaml',
                'h5py',
                'toml',
                'pytest',
                'pytest-runner']

setup_requirements = ['pytest-runner', 'pytest']

test_requirements = ['pytest-runner', 'pytest']

setup(
    author="Adam Reay Lamson",
    author_email='alamson@flatironinstitute.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Python module to create, schedule, and analyze simulations on computing clusters.",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chi_pet',
    name='chi_pet',
    packages=find_packages(include=['chi_pet']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/lamsoa729/chi_pet',
    version='0.1.0',
    zip_safe=False,
    entry_points={'console_scripts': ['Chi = chi_pet.chi:main', ], }
)
