from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("filters/cv_filters_c.pyx"))
