import setuptools

setuptools.setup(
    name="iatikit",
    version="0.0.0",
    description="",
    long_description="",
    url="https://github.com/IATI/IATI-Kit",
    packages=setuptools.find_packages(exclude=["test"]),
    install_requires=[
        "lxml",
        "requests",
    ],
    extras_require={
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
