from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='django_simple_forum',
      version=version,
      description="Django simple forum",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Urtzi Odriozola',
      author_email='urtzi.odriozola@gmail.com',
      url='',
      license='cc-by-sa',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Django >= 1.10',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
