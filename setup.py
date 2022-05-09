from setuptools import setup
import _version

def readme():
    with open("README.md") as f:
        return f.read()

setup(
    name="Clappform",
    version=_version.__version__,
    description="Clappform API Connector",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/DiegoTolenClappform/Clappform-Python-Connector",
    download_url = 'https://github.com/DiegoTolenClappform/Clappform-Python-Connector/archive/' + _version.__version__ + '.tar.gz',
    author="Clappform",
    author_email="info@clappform.com",
    keywords="api connector",
    license="MIT",
    packages = ['Clappform'],
    install_requires=[
        "pandas",
        "PyGithub",
        "pyarrow"
    ],
    include_package_data=True,
)
