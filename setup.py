from setuptools import setup

setup(name='libhpc-cf',
      version='0.4',
      description='Libhpc coordination forms and components library',
      url='https://www.github.com/london-escience/libhpc-cf',
      author='Jeremy Cohen',
      author_email='jeremy.cohen@imperial.ac.uk',
      license='BSD 3-Clause',
      packages=['libhpc','libhpc.cf','libhpc.component','libhpc.wrapper','libhpc.wrapper.bio'],
      zip_safe=False)

