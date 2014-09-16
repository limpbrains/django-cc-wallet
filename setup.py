from setuptools import setup, find_packages
from os.path import join, dirname


setup(
    name='django-cc-wallet',
    version='0.0.1',
    license='BSD License',
    description='Example of django-cc wallet for Bitcoin and other cryptocurrencies',
    author='Ivan',
    keywords='bitcoin litecoin django django-cc wallet',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    install_requires=[
        'django-cc'
    ]
)
