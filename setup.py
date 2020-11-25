import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="takprotobuf",
    version="0.0.1",
    author="Delta Bravo-15",
    author_email="deltabravo15ga@gmail.com",
    description="A Python library to encode and decode Cursor-on-Target (CoT) messages using Protocol Buffers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DeltaBravo15/takprotobuf",
	keywords=['TAK', 'ATAK', 'WinTAK', 'Python', 'Opensource'],
    packages=setuptools.find_packages(),
	install_requires=[
		'untangle',
		'lxml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
