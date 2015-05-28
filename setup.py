from distutils.core import setup
import pyTenvis

setup( name='pyTenvis',
    version=pyTenvis.__version__,
    maintainer='Simon Bilgeri',
    maintainer_email='Simon.Bilgeri@gmx.de',
    packages=find_packages(),
    include_package_data=True,
    scripts=[],
    url='https://github.com/SimBil91/pyTenvis',
    download_url = 'https://github.com/SimBil91/pyTenvis/tarball/0.1',
    description='Library for Tenvis HD IPCAMs',
      )
