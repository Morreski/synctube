from setuptools import setup

setup(
    name='synctube',
    version='0.0.1-dev',
    description='Youtube remote control service',
    url='',
    author='Enguerrand Pelletier',
    author_email='epelletier@protonmail.com',
    license='GNU GPLv3',
    packages=['synctube'],
    install_requires=['tornado==4.3'],
    include_package_data = True,
    entry_points={
        'console_scripts': ['synctube=synctube.app:main']
    }
)
