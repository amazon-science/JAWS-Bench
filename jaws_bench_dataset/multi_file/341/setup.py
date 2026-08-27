from setuptools import setup, find_packages

setup(
    name='TrojanCockroach',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'pywin32',
    ],
    entry_points={
        'console_scripts': [
            'trojan_cockroach=main:main',
        ],
    },
)