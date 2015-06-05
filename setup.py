from distutils.core import setup

setup(
    name='AStarRoute',
    version='0.95a',

    packages=[
        'AStarRoute',
    ],

    package_data={
        'AStarRoute': ['defaults.cfg'],
    },

    install_requires=[
        'numpy',
        'pygame'
    ]
)

