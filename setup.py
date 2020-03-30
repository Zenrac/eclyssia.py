from setuptools import setup

setup(
    name='eclyssia',
    packages=['eclyssia'],
    version='1.2.1',
    description='An eclyssia-api wrapper built for python3+',
    author='Zenrac',
    author_email='zenrac@outlook.fr',
    url='https://github.com/Zenrac/eclyssia.py',
    download_url='https://github.com/Zenrac/eclyssia.py/archive/1.2.1.tar.gz',
    keywords=['eclyssia'],
    include_package_data=True,
    install_requires=['aiohttp']
)
