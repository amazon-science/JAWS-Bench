from setuptools import setup, find_packages

# Setup script to create a deployable package
setup(
    name='keyboard_hook',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pyHook',
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'keyboard_hook=keyboard_hook:main',
        ],
    },
)