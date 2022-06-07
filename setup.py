from setuptools import setup, find_packages

VERSION_FILE = "__version__.txt"
short_description = 'Mutamorhpic testing tool for text-based machine learning problems.'

try:
    file = open("README.md")
    long_description = file.read()
except:
    long_description = short_description

version = None
try:
    version = open(VERSION_FILE).read()\
        .strip()\
        .replace("v", "")\
        .replace("-test", "")
except:
    exit("mutamorphic-test publishing error: Version file not found")

setup(
    name='mutamorphic-test',
    version=version,
    description=short_description,
    author="Maarten van Tartwijk",
    author_email='m.j.vantartwijk@student.tudelft.nl',
    packages=find_packages(include=['mutatest']),
    include_package_data=True,
    project_urls={
        'Source': 'https://github.com/Maarten0110/mutatest',
    },
    url='https://github.com/Maarten0110/mutatest',
    keywords='machine learning testing mutamorphic',
    install_requires=[
        'numpy',
        'nltk',
    ],
    python_requires='>=3.7',
    long_description=long_description,
    long_description_content_type="text/markdown",
)
