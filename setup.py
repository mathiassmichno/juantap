from setuptools import setup

setup(
    name='juantap',
    version='0.1',
    packages=['juantap'],
    install_requires=[
        'click',
        'sh'
    ],
    entry_points='''
        [console_scripts]
        juantap=juantap:cli
    ''',
)
