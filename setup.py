import os
from setuptools import setup


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


setup(name='timy',
      version='0.4.2',
      description='Minimalist measurement of python code time',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      url='https://github.com/ramonsaraiva/timy',
      author='Ramon Saraiva',
      author_email='ramonsaraiva@gmail.com',
      license='MIT',
      packages=['timy'],
      zip_safe=False)
