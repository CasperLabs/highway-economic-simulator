import os

from setuptools import setup, find_packages

# Meta information
# version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)

# Save version and author to __meta__.py
# path = os.path.join(dirname, 'src', 'economic-simulator', '__meta__.py')
# data = '''# Automatically created. Please do not edit.
# __version__ = u'%s'
# __author__ = u'F\\xe1bio Mac\\xeado Mendes'
# ''' % version
# with open(path, 'wb') as F:
#     F.write(data.encode())

setup(
    # Basic info
    name="highway_economic_simulator",
    # version=version,
    author="Onur Solmaz",
    author_email="onur@casperlabs.io",
    url="",
    description="",
    # long_description='',
    classifiers=[],
    # Packages and depencies
    # package_dir={'': 'highway_economic_simulator'},
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    # packages=find_packages('highway_economic_simulator'),
    install_requires=[
        "numpy",
        "progressbar2",
        "sortedcontainers",
    ],
    # extras_require={
    #     'dev': [
    #     ],
    # },
    # Data files
    # package_data={
    #     'highway_economic_simulator': [
    #         'templates/*.*',
    #         'templates/license/*.*',
    #         'templates/docs/*.*',
    #         'templates/package/*.*'
    #     ],
    # },
    # Scripts
    # entry_points={
    #     'console_scripts': [
    # },
    # Other configurations
    zip_safe=False,
    platforms="any",
)
