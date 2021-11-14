README = """
Crypto trading program.
"""

setup(
    name="CryptoGraph",
    version="1.0.0",
    description="Crypto trading program.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/realpython/reader",
    author="Rhys Adams",
    author_email="rhys@therhys.co.uk",
    license="GPLv2",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=["CryptoGraph"],
    include_package_data=True,
    install_requires=[
        "pygobject", "cryptocompare", "matplotlib"
    ],
    entry_points={"console_scripts": ["cryptograph=CryptoGraph.__main__:main"]},
)
