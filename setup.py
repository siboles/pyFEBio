'''
Created on 2013-05-15

@author: Scott Sibole
'''
from distutils.core import setup

setup(
    name = 'febio',
    version = '1.0.0',
    packages = ['febio',],
    py_modules = ['febio.__init__','febio.MatDef','febio.MeshDef','febio.Boundary','febio.Control','febio.Load','febio.Model'],
    author = 'Scott Sibole',
    author_email = 'ssibole@kin.ucalgary.ca',
    license = 'MIT',
    package_data = {'febio': ['verification/*'],},
    download_url = 'https://github.com/siboles/',
    description = 'A Python API for FEBio',
)
