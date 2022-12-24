from glob import glob
from setuptools import setup, find_packages
from pybind11.setup_helpers import Pybind11Extension, build_ext, ParallelCompile, naive_recompile

ParallelCompile("NPY_NUM_BUILD_JOBS", needs_recompile=naive_recompile).install()

__version__ = '0.0.1'

ext_modules = [
    Pybind11Extension(
        "pybind11_example",
        sorted(glob("src/*.cpp")),
        define_macros = [('VERSION_INFO', __version__)]
    ),
]

setup(
    name='pybind11-example',
    version=__version__,
    description='example in how to use pybind11',
    author='senseis',
    author_email='senseisworkspace@gmail.com',
    url='',
    packages=find_packages(exclude=['']),
    package_data={},
    data_files={},
    install_requires=[
        'pybind11',
        'scikit-learn',
    ],
    entry_points={
      'console_scripts':[
          'measure_summation = senseis.measure_summation:main',
          'measure_linear_regression = senseis.measure_linear_regression:main',
      ]
    },
    scripts=[],
    ext_modules=ext_modules,
    cmdclass={"build_ext" : build_ext},
    python_requires=">3.7",
    zip_safe=False,
)
