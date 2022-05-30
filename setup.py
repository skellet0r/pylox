import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

requirements = list(map(str.strip, (here / "requirements.txt").read_text().split("\n")))[:-1]

setup(
    name="pylox",
    version="0.1.0",
    description="Python implementation of the Lox interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skellet0r/pylox",
    packages=find_packages(),
    python_requires=">=3.10, <4",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pylox = pylox.__main__:main",
        ],
    },
)
