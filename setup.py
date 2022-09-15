from setuptools import setup
import Clappform


url = "https://github.com/DiegoTolenClappform/Clappform-Python-Connector"


def readme():
    with open("README.md") as fd:
        return fd.read()


setup(
    name="Clappform",
    version=Clappform.__version__,
    description="Clappform API Connector",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url=url,
    download_url="{}/archive{}{}".format(
        url,
        Clappform.__version__,
        ".tar.gz",
    ),
    author=Clappform.__author__,
    author_email=Clappform.__email__,
    keywords="api connector",
    license=Clappform.__license__,
    packages=["Clappform"],
    install_requires=["PyGithub", "numpy", "pandas", "pyarrow", "redis", "requests"],
    include_package_data=True,
)
