from setuptools import setup, find_packages

with open('requirements.txt') as fp:
    install_requires = fp.readlines()

setup(
    name='export-lib',
    packages=find_packages(),
    version='0.1',
    description='Export data tool',
    author='BMAT Developers',
    url='',
    download_url='',
    classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
    install_requires=install_requires
)
