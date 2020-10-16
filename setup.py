from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='dataimport',
    version='0.1.0',
    author='David Buckley',
    author_email='david@davidbuckley.ca',
    url='https://github.com/buckley-w-david/dataimport',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='read datafiles via the import system',
    packages=find_packages()
)
