from setuptools import setup

with open("README.md", encoding="utf-8") as rm:
    readme = rm.read()

setup(
    name="nasawrapper",
    author="End313234",
    url="https://github.com/End313234/nasawrapper",
    project_urls={
        "Bug Hunter": "https://github.com/End313234/nasawrapper/issues"
    },
    version="0.0.1",
    license="MIT",
    description="A wrapper for NASA APIs",
    long_description=readme,
    long_description_content_type="text/markdown",
    python_requires=">=3.8.0",
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Topic :: Internet"
    ],
    package_dir={"": "src"}
)