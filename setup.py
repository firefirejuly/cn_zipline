#!/usr/bin/env python

from setuptools import setup, find_packages


try:
    import pypandoc

    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = ''


setup(
    name='cn_zipline',
    version='0.02',
    description='china zipline bundles',
    long_description=long_description,
    author='Jie Wang',
    author_email='790930856@qq.com',
    url='https://github.com/JaysonAlbert/cn_zipline',
    packages=find_packages(include=['cn_zipline', 'cn_zipline.*']),
    entry_points={
        'console_scripts': [
            'cn_zipline = cn_zipline.__main__:main',
        ],
    },
    install_requires=[
        'pytdx',
        'cn-treasury_curve',
        'zipline',
    ]
)
