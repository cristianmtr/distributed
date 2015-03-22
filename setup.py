#!/usr/bin/python

from distutils.core import setup
from distutils.extension import Extension

setup(name="PackageName",
      ext_modules=[
          Extension("module", ["module.cpp"],
                    libraries = ["boost_python"])
      ])
