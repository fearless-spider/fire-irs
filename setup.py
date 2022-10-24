"""
Module packaging
"""

from setuptools import find_packages, setup

REQUIRES = ["click", "jsonschema"]
TEST_REQUIRES = [
    "pytest-runner>=6.0.0",
    "black>=22.6.0",
    "flake8>=5.0.4",
    "isort>=5.10.1",
    "pytest>=7.1.2",
    "pytest-runner>=6.0.0",
    "pytest-isort>=3.0.0",
    "pytest-black>=0.3.12",
    "pytest-flake8>=1.1.1",
]

DOCS_REQUIRES = [
    "Sphinx",
    "docutils",
    "repoze.sphinx.autointerface",
]

setup(
    name="fire-irs",
    description="Generate IRS files for transmission through the \
    IRS FIRE system",
    long_description=open("README.md").read(),
    license="MIT",
    author="Stephen Johnson, Przemyslaw Pajak",
    author_email="4stephen.j@gmail.com, office@fearlessspider.com",
    url="https://github.com/fearless-spider/fire-irs",
    version="1.0.0",
    packages=find_packages(exclude=["contrib", "docs", "tests*", "spec*"]),
    include_package_data=True,
    install_requires=REQUIRES,
    extras_require={"tests": TEST_REQUIRES, "docs": DOCS_REQUIRES},
    scripts=["bin/fire-irs"],
    classifiers=[
        "Development Status :: 4 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
