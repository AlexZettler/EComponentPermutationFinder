from setuptools import find_packages, setup

from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ECPF',
    version='0.1',
    author="Alexander Zettler(@AlexZettler)",
    author_email="azettler@live.com",
    description="Simplifies the process of finding passive components for a schematic.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/AlexZettler/EComponentPermutationFinder",
    packages=[
        'ECPF'
    ],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
