import os

from setuptools import find_packages, setup

from printy import __version__

readme_path = os.path.join(os.path.dirname(__file__), "README.md")
with open(readme_path) as fh:
    long_description = fh.read()

setup(
    name="printy",
    version=__version__,
    url="https://github.com/edraobdu/printy",
    author="Edgardo Obregón",
    author_email="edraobdu@gmail.com",
    description="Colorize the print statement by global or inline flags",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.5'
)
