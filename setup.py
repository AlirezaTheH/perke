from os.path import join
from setuptools import (setup,
                        find_packages)

packages = find_packages(exclude=['tests*'])

with open('requirements.txt') as f:
    requirements = f.read().split()

with open('README.md') as f:
    long_description = f.read()

filename = join('perke', 'version.py')
with open(filename) as f:
    exec(compile(f.read(), filename, 'exec'))


setup(name='perke',
      version=__version__,
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
