import re
from pathlib import Path

from setuptools import find_packages, setup

requirements_path = Path('requirements')
with open(requirements_path / 'main.txt') as f:
    requirements = f.read().split()

extras_requirements = {}
for extra in requirements_path.iterdir():
    if not extra.name.endswith('main.txt'):
        with open(extra) as f:
            extras_requirements[extra.name[:-4]] = f.read().split()

with open('README.md') as f:
    long_description = f.read()

with open(Path('perke') / 'version.py') as f:
    version = re.search(
        r'__version__\s=\s\'(?P<version>.*)\'', f.read()
    ).group('version')

setup(
    name='perke',
    version=version,
    description='A keyphrase extractor for Persian',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alirezatheh/perke',
    project_urls={
        'Bug Tracker': 'https://github.com/alirezatheh/perke/issues',
        'Documentation': 'https://perke.readthedocs.io',
        'Source Code': 'https://github.com/alirezatheh/perke',
    },
    author='Alireza Hosseini',
    author_email='alirezatheh@gmail.com',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    entry_points={'console_scripts': ['perke = perke.cli:setup_cli']},
    keywords=[
        'nlp',
        'natural-language-processing',
        'information-retrieval',
        'computational-linguistics',
        'persian-language',
        'persian-nlp',
        'persian',
        'keyphrase-extraction',
        'keyphrase-extractor',
        'keyphrase',
        'keyword-extraction',
        'keyword-extractor',
        'keyword',
        'machine-learning',
        'ml',
        'unsupervised-learning',
    ],
    install_requires=requirements,
    python_requires='>=3.8',
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
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Natural Language :: Persian',
    ],
)
