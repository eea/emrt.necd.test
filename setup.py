# -*- coding: utf-8 -*-
"""Installer for the emrt.necd.test package."""

from setuptools import find_packages
from setuptools import setup


LONG_DESCRIPTION = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])


setup(
    name='emrt.necd.test',
    version='1.0a1',
    description="Necd testing metapackage",
    long_description=LONG_DESCRIPTION,
    # Get more from https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5.2",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    keywords='Python Plone',
    author='Irina Botez',
    author_email='irina.botez@eaudeweb.ro',
    url='https://pypi.python.org/pypi/emrt.necd.test',
    license='GPL version 3',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['emrt'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'edw.seleniumtesting',
    ],
    entry_points={
        'edw.seleniumtesting': [
            'emrt.necd.test.setup_tests = emrt.necd.test.setup_tests:suite',
            'emrt.necd.test.review_folder = emrt.necd.test.review_folder:suite',
            'emrt.necd.test.finish_observation = emrt.necd.test.finish_observation:suite',
            'emrt.necd.test.deny_observation = emrt.necd.test.deny_observation:suite',
            'emrt.necd.test.add_answer = emrt.necd.test.add_answer:suite',
            'emrt.necd.test.finish_observation_lr = emrt.necd.test.finish_observation_lr:suite',
            'emrt.necd.test.ask_to_redraft = emrt.necd.test.ask_to_redraft:suite',
            'emrt.necd.test.add_conclusions = emrt.necd.test.add_conclusions:suite',
            'emrt.necd.test.remove_test_site = emrt.necd.test.remove_test_site:suite',
        ]
    }
)

