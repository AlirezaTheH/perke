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
      url='https://github.com/alirezah320/perke',
      author='Alireza Hosseini',
      author_email='alirezah320@yahoo.com',
      packages=packages,
      description='A keyphrase extractor for Persian',
      long_description=long_description,
      long_description_content_type='text/markdown',
      license='MIT',
      install_requires=requirements)
