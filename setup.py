import re
import os
from setuptools import (setup,
                        find_packages)

packages = find_packages(exclude=['tests*'])

with open('requirements.txt') as f:
    requirements = f.read().split()

with open('README.md') as f:
    long_description = f.read()

with open(os.path.join('perke', 'version.py')) as f:
    version_pattern = re.compile(r'__version__\s+=\s+\'(?P<version>.*)\'')
    version = re.search(version_pattern, f.read()).group('version')


setup(name='perke',
      version=version,
      description='A keyphrase extractor for Persian',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/alirezah320/perke',
      author='Alireza Hosseini',
      author_email='alirezah320@yahoo.com',
      packages=packages,
      license='MIT',
      install_requires=requirements,
      python_requires='>=3.6',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
      ])
