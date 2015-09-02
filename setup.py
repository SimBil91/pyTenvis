from setuptools import setup, find_packages

setup( name='pyTenvis',
    version=0.12,
    author = 'Simon Bilgeri',
    author_email = 'Simon.Bilgeri@tum.de',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/SimBil91/pyTenvis',
    download_url = 'https://github.com/SimBil91/pyTenvis/tarball/0.12',
    description='Library for Tenvis HD IPCAMs',
    keywords = ['TENVIS', 'IPCAM', 'library'])
