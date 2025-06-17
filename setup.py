import os

from setuptools import find_packages, setup

version = "1.127.1"

current_directory = os.path.abspath(os.path.dirname(__file__))
readme_file_location = os.path.join(current_directory, "README.md")

try:
    with open(readme_file_location, encoding="utf-8") as readme_file:
        long_description = readme_file.read()
except FileNotFoundError:
    long_description = ""

setup(
    name="politecheck-api",
    version=version,
    description="Publicly exposed politecheck API",
    author="Mohamed Salem",
    python_requires=">=3.12",
    package_dir={"": "src"},
    package_data={"": ["*.yml"]},
    packages=find_packages(where="src"),
    platforms=["Linux", "Mac OS"],
    # url="https://bitbucket.org/,
    long_description=long_description,
    long_description_content_type="text/markdown",
    zip_safe=False,
    install_requires=[
        "pyramid",
        "gunicorn",
        "waitress",
        "pyyaml",
    ],
    entry_points={
        "paste.app_factory": [
            "main = politecheck:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
            "black",
            "isort",
            "flake8",
        ],
    },
)
