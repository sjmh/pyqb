from setuptools import setup

setup(name='pyqb',
      version='0.2.1',
      description='Quickbase API Python Wrapper',
      url='http://github.com/sjmh/pyqb',
      author='Steven Hajducko',
      author_email='steven_hajducko@intuit.com',
      license='EPL-1.0',
      classifiers=[
                  'Development Status :: 3 - Alpha',
                  'Intended Audience :: Developers',
                  'Environment :: Console',
                  'Operating System :: POSIX :: Linux',
                  'Operating System :: MacOS :: MacOS X',
                  'Topic :: Software Development :: Libraries',
                  'Programming Language :: Python :: 2',
                  'Programming Language :: Python :: 2.6',
                  'Programming Language :: Python :: 2.7'
      ],
      keyworks=['quickbase'],
      packages=['pyqb'],
      install_requires=[
          'xmltodict',
          'requests'
      ],
      zip_safe=False)
