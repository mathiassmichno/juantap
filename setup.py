from setuptools import setup

setup(
    name='lgsmutil',
    version='0.1',
    py_modules=['lgsmutil'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        lgsmutil=lgsmutil:cli
    ''',
)
