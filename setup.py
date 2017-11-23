from setuptools import setup, find_packages

setup(
    name='swc_parser',
    version='0.0.1',
    author='Cassandra Jacobs',
    author_email='jacobs.cassandra.l@gmail.com',
    license='CC',
    url='https://github.com/BayesForDays/swc_parser',
    description='Functions for creating your own nontological `embeddings`',
    packages=find_packages(),
    long_description='Functions for creating your own nontological `embeddings`',
    keywords=['xml', 'spoken_wikipedia', 'corpora'],
    classifiers=[
        'Intended Audience :: Developers',
    ],
    install_requires=[
        'xmltodict',
        'pandas',
        'click'
    ]
)