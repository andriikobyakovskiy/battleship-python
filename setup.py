from setuptools import setup, find_packages

setup(
      name='battleship',
      version='0.0.1',
      packages=find_packages(
            include=['battleship/*'],
            exclude=['battleship.test'],
      ),
)
