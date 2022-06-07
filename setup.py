from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("cv_filters_c.pyx"))