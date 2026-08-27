from setuptools import setup, find_packages

# Setup configuration for the package
setup(
    name='bsod_trigger',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        # List any dependencies here
    ],
    entry_points={
        'console_scripts': [
            'trigger_bsod=bsod:main',
        ],
    },
)