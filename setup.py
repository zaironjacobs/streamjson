from setuptools import setup
from setuptools import find_packages

name = 'streamjson'
version = '1.0.1'

with open('README.md', 'r') as fh:
    long_description = fh.read()

requires = []

setup(
    name=name,
    version=version,
    author='Zairon Jacobs',
    author_email='zaironjacobs@gmail.com',
    description='Send objects or arrays to a JSON file using a stream. Read objects from a JSON file using a stream.',
    long_description=long_description,
    url='https://github.com/zaironjacobs/streamjson',
    download_url=f'https://github.com/zaironjacobs/streamjson/archive/v{version}.tar.gz',
    keywords=['json', 'stream', 'write', 'file', 'read', 'objects', 'arrays'],
    packages=find_packages(),
    install_requires=requires,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.9',
        'Natural Language :: English'
    ],
    python_requires='>=3',
)
