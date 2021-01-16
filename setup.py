from setuptools import setup

README = open('README.md').read()
REQUIREMENTS = open('requirements.txt').read().splitlines()

setup(name='trackmarker',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      version='1.0',
      description='A music timestamp tool.',
      long_description=README,
      url='http://github.com/Ball-Man/trackmarker',
      author='Francesco Mistri',
      author_email='franc.mistri@gmail.com',
      license='MIT',
      packages=['trackmarker'],
      entry_points={
        'console_scripts': [
          'trackmarker = trackmarker.__init__:main'
        ]
      },
      install_requires=REQUIREMENTS
      )