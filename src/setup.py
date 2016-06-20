from setuptools import setup

setup(name='clouderasizer',
      version='0.1',
      description='Multipurpose tool for collecting and demonstrating metrics from a Cloudera Hadoop cluster',
      url='http://github.com/bkvarda/clouderasizer',
      author='Brandon Kvarda',
      author_email='bjkvarda@gmail.com',
      license='MIT',
      packages=['clouderasizer'],
      install_requires=[
          'python-pptx',
          'cm-api'
       ],
      zip_safe=False)
