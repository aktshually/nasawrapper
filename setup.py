from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as rm:
    readme = rm.read()

requirements = []
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="nasawrapper",
    author="End313234",
    url="https://github.com/End313234/nasawrapper",
    project_urls={
        "Bug Hunter": "https://github.com/End313234/nasawrapper/issues",
        "Documentation": "https://nasawrapper.readthedocs.io/en/latest/"
    },
    version="0.3.2",
    license="MIT",
    description="A simple wrapper to fetch NASA Open APIs using Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Topic :: Internet",
        "Development Status :: 3 - Alpha"
    ],
    packages=find_packages(),
    install_requires=requirements
)