from setuptools import find_packages
from setuptools import setup


with open("README.md") as f:
    LONG_DESCRIPTION = f.read()


def get_install_requires():
    with open("requirements.txt", "r") as f:
        return [line.strip() for line in f.readlines() if not line.startswith("-")]


setup(
    name="ehva",
    version="0.0.3",
    url="https://github.com/EHVAAutomation/ehva-python",
    license="MIT",
    author="ehva Inc.",
    author_email="info@ehva.ca",
    description="Library used to run Python scripts from the EHVA Ap",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=("tests",)),
    install_requires=get_install_requires(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ],
)
