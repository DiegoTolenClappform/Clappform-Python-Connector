from setuptools import setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="Clappform",
    version="1.0.4",
    description="Clappform API Connector",
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/joeyhoek/Clappform-Python-Connector",
    download_url = 'https://github.com/joeyhoek/Clappform-Python-Connector/archive/1.0.3.tar.gz', 
    author="JoeyHoek",
    author_email="j.hoek@clappform.com",
    keywords="api connector",
    license="MIT",
    packages = ['Clappform'],
    install_requires=[
        "pandas"
    ],
    include_package_data=True,
)