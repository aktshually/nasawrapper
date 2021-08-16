from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as rm:
    readme = rm.read()

setup(
    name="nasawrapper",
    author="End313234",
    url="https://github.com/End313234/nasawrapper-python",
    project_urls={
        "Bug Hunter": "https://github.com/End313234/nasawrapper-python/issues",
        "Documentation": "https://github.com/End313234/nasawrapper-python#documentation"
    },
    version="0.0.5",
    license="MIT",
    description="A wrapper for NASA APIs",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.6.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Topic :: Internet"
    ],
    packages=find_packages()
)