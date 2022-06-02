from setuptools import setup, find_packages

short_description = 'Mutamorhpic testing tool for text-based machine learning problems.'

try:
    file = open("README.md")
    long_description = file.read()
except:
    long_description = short_description

setup(
    name='mutamorphic-test',
    version='0.1.0',
    description=short_description,
    author="Maarten van Tartwijk",
    author_email='m.j.vantartwijk@student.tudelft.nl',
    packages=find_packages(include=['mutatest']),
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
