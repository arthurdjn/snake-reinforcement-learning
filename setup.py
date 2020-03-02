# -*- coding: utf-8 -*-
# Created on Wed Jan 29 00:11:30 2020
# @author: arthurd


from setuptools import setup, find_packages


def readme_data():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


find_packages()

setup(name='pysnake',
        version = '0.1',
        description = 'AI learns to play snake game.',
        long_description = readme_data(),
        long_description_content_type = "text/markdown",
        url = 'https://github.uio.no/arthurd/pysnake',
        author = 'Arthur Dujardin',
        author_email = 'arthur.dujardin@ensg.eu',
        license = 'Apache License-2.0',

        install_requires = ['pygame', 'numpy', 'json'],
        packages = find_packages(),
        zip_safe  = False,
        classifiers = [
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
    
        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Deep Learning and Genetic Algorithm',
    
        # Pick your license as you wish (should match "license" above)
    
        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        ]
    )


