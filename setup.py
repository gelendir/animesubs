from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='animesubs',
      version=version,
      description="small lib for managing animesubs related stuff",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Gregory Eric Sanderson',
      author_email='gzou2000@gmail.com',
      url='http://github.com/gelendir/animesubs',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "pyyaml",
          "feedparser",
      ],
      entry_points={
          'console_scripts': [
              "download_feeds = animesubs.bin.download_feeds:main"
          ]
      }
      )
