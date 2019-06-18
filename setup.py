#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='django-rest-framework-google-json-style-api',
    version='1.0.0',
    description="Make Google Json Style and Django Rest Framework play nice together.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Pocheng, Scott",
    author_email='pcghuang@gmail.com, scott820914@gmail.com',
    url='https://github.com/Envive',
    license='BSD License',
    packages=find_packages(),
    package_data={'rest_framework_google_json_style_api': []},
    test_suite="example.settings.test",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'django',
        'djangorestframework',
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
