from setuptools import setup

setup(name='pyqb',
      version='0.1.2',
      description='Quickbase API Python Wrapper',
      url='http://intuit.github.com/shajducko/pyqb',
      author='Steven Hajducko',
      author_email='steven_hajducko@intuit.com',
      license='EPL-1.0',
      packages=['pyqb'],
      install_requires=[
          'xmltodict',
          'requests'
      ],
      zip_safe=False)
