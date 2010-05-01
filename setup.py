from setuptools import setup, find_packages

version = '0.1.6'

setup(
    name = 'FuncBrows',
    version = version,
    description = 'Web functional testing abstraction layer',
    long_description = open("README.rst").read(),
    url = "http://pypi.python.org/pypi/funcbrows",
    classifiers = ["Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Programming Language :: Python"],
    keywords = "functional test web browser",
    author = "Tom Wardill",
    author_email = "tom.wardill@isotoma.com",
    license = "BSD License",
    packages = find_packages(exclude=['ez_setup']),
    package_dir = {'FuncBrows': 'FuncBrows'},
    package_data = {
        '':['README.rst'],
        'FuncBrows': ['test.html']
    },
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'zc.testbrowser'
    ]
)
