from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='animesubs',
      version=version,
      description="small lib for managing anime torrent feeds",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gregory Eric Sanderson',
      author_email='gzou2000@gmail.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )