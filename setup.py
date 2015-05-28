from distutils.core import setup
import setuptools
import pyTenvis

setup( name='pyTenvis',
    version=pyTenvis.__version__,
    author = 'Simon Bilgeri',
    author_email = 'Simon.Bilgeri@tum.de',
    include_package_data=True,
    url='https://github.com/SimBil91/pyTenvis',
    download_url = 'https://github.com/SimBil91/pyTenvis/tarball/0.1',
    description='Library for Tenvis HD IPCAMs',
    keywords = ['TENVIS', 'IPCAM', 'library'])