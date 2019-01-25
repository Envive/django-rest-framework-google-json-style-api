#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='rest_framework_google_json_style_api',
    version='0.0.1',
    description="Make Google Json Style and Django Rest Framework play nice together.",
    author="Pocheng, Scott",
    author_email='phuang@enviveus.com, schang@enviveus.com',
    url='http://www.enviveus.com',
    packages=find_packages(),
    package_data={'rest_framework_google_json_style_api': []},
    test_suite="example.settings.test",
    install_requires=[
        'django',
        'django-rest-framework',
        'django-rest-framework-camel-case',
        'inflection'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'django-debug-toolbar',
        'pytest',
        'pytest_django',
        'pytest_factoryboy',
        'pytest-cov',
    ]
)
