from setuptools import find_packages, setup

with open("README.md") as readme_file:
    README = readme_file.read()

setup(
    name="pynamodb-plus",
    version="0.0.4",
    author="Murilo Viana",
    author_email="murilo.vianamo@gmail.com",
    description="Python 3 library with some utilities to use with PynamoDB",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MaisTodos/pynamodb-plus",
    packages=find_packages(exclude=["tests"]),
    zip_safe=False,
    keywords="python pynamodb plus",
    license="MIT License",
    install_requires=["pynamodb>=4.0.0"],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
    ],
)
