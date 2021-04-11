import re
from os.path import join

from setuptools import find_packages, setup

packages = find_packages(exclude=['tests*'])

with open(join('requirements', 'default.txt')) as f:
    requirements = f.read().split()

with open('README.md') as f:
    long_description = f.read()

with open(join('perke', 'version.py')) as f:
    version_pattern = re.compile(r'__version__\s+=\s+\'(?P<version>.*)\'')
    version = re.search(version_pattern, f.read()).group('version')

setup(name='perke',
      version=version,
      description='A keyphrase extractor for Persian',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/alirezah320/perke',
      project_urls={
          'Bug Tracker': 'https://github.com/alirezah320/perke/issues',
          'Documentation': 'https://perke.readthedocs.io',
          'Source Code': 'https://github.com/alirezah320/perke',
      },
      author='Alireza Hosseini',
      author_email='alirezah320@yahoo.com',
      packages=packages,
      keywords=[
          'nlp',
          'natural language processing',
          'information retrieval',
          'computational linguistics',
          'persian language',
          'persian nlp',
          'persian',
          'keyphrase extraction',
          'keyphrase extractor',
          'keyphrase',
          'keyword extraction',
          'keyword extractor',
          'keyword',
      ],
      install_requires=requirements,
      python_requires='>=3.6',
      classifiers=[
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Scientific/Engineering :: Human Machine Interfaces',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Topic :: Text Processing',
          'Topic :: Text Processing :: Filters',
          'Topic :: Text Processing :: General',
          'Topic :: Text Processing :: Indexing',
          'Topic :: Text Processing :: Linguistic',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Operating System :: OS Independent',
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'Intended Audience :: Information Technology',
          'Intended Audience :: Science/Research',
          'Natural Language :: Persian',
      ])
