from setuptools import setup, find_packages

setup(name='proglan',
      version='0.1',
      description='CS403 Designer Programming Language',
      author='Richard Belleville',
      author_email='rjbelleville@crimson.ua.edu',
      setup=['bin/proglan'],
      # packages=find_packages(exclude=["test_*"])
      packages=['proglan.lexer', 'proglan.parser', 'proglan.environment', 'proglan.printer']
      )
