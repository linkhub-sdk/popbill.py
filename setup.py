from __future__ import print_function

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys

version = '1.16.0'

if sys.version_info <= (2, 5):
    error = "ERROR: popbill requires Python Version 2.6 or above...exiting."
    print(error, file=sys.stderr)
    sys.exit(1)

setup(name = "popbill",
      version = version,
      description = "Popbill API SDK Library",
      long_description = "Popbill API SDK. Consist of Taxinvice Service. http://www.popbill.com",
      author = "Kim Seongjun",
      author_email = "pallet027@gmail.com",
      url = "https://github.com/linkhub-sdk/Popbill.py",
      download_url = "https://github.com/linkhub-sdk/Popbill.py/archive/"+version+".tar.gz",
      packages = ["popbill"],
      install_requires=[
          'linkhub',
      ],
      license = "MIT",
      platforms = "Posix; MacOS X; Windows",
      classifiers = ["Development Status :: 5 - Production/Stable",
                     "Intended Audience :: Developers",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                     "Topic :: Internet",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.6",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.3",
                     "Programming Language :: Python :: 3.4",
                     "Programming Language :: Python :: 3.5",
                     "Programming Language :: Python :: 3.6",
                     "Programming Language :: Python :: 3.7"]
      )
