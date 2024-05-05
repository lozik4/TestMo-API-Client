from setuptools import setup, find_packages

setup(
    name='TestMoApiClient',
    version='0.0.1',
    packages=find_packages(),
    description='This library wrapper to TestMo API',
    long_description=open('README.md').read(),
    author='Serhii Lozytskyi',
    url='https://github.com/lozik4/TestMo-API-Client',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'requests',
    ],
)
