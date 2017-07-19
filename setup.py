from setuptools import setup

setup(
    name='juantap',
    version='0.1',
    py_modules=['juantap'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        juantap=juantap:cli
    ''',
)
