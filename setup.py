#!/usr/bin/env python
import os
import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand

import queryfilter

tests_requires = [
    'pytest==3.0.3',
    'pytest-cov==2.4.0',
]


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['tests', '--cov=queryfilter', '-vrsx']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


def readme():
    try:
        os.system('pandoc --from=markdown --to=rst README.md -o README.rst')
        with open('README.rst') as f:
            return f.read()
    except:
        return '''PyConst one simple way to organize the constants'''


setup(name='sqlalchemy_queryfilter',
      url='https://github.com/valdergallo/sqlalchemy_queryfilter',
      download_url='https://github.com/valdergallo/sqlalchemy_queryfilter/tarball/%s/' % pyconst.get_version(),
      author="valdergallo",
      author_email='valdergallo@gmail.com',
      keywords=['api', 'sqlalchemy', 'queryfilter', 'rest'],
      description='Sqlalchemy Queryfilter create default process to use REST filters',
      license='GPL-3.0',
      long_description=readme(),
      classifiers=[
          'Framework :: Django',
          'Operating System :: OS Independent',
          'Topic :: Utilities',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
      ],
      include_package_data=True,
      version=queryfilter.get_version(),
      tests_require=tests_requires,
      cmdclass={'test': PyTest},
      packages=['queryfilter'],
      zip_safe=False,
      platforms='any',
)
