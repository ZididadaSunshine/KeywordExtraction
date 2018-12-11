from setuptools import setup
from setuptools import find_packages


setup(
    name='KeywordExtraction',
    version='1.4',
    packages=find_packages(),
    url='https://github.com/ZididadaSunshine/KeywordExtraction',
    license='',
    author=' Zididada Sunshine',
    install_requires=['gensim',
                      'beautifulsoup4',
                      'numpy',
                      'nltk',
                      'contractions',
                      'networkx'],
    author_email='sw704e18@cs.aau.dk',
    description=''
)
