from distutils.core import setup

setup(name='perke',
      version='0.1.0',
      description='Persian Keyphrase Extraction module',
      author='Alireza Hosseini',
      author_email='alirezah320@yahoo.com',
      license='gnu',
      packages=['perke', 'perke.unsupervised',
                'perke.unsupervised.graph_based'],
      url="https://github.com/alirezah320/perke",
      install_requires=[
          'hazm',
          'networkx',
          'scipy',
      ],
      package_data={'perke': ['resources/*.model']}
      )