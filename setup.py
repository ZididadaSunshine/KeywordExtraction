from setuptools import setup
from setuptools import find_packages


setup(
    name='kwe',
    version='1.0',
    packages=find_packages(),
    url='https://github.com/ZididadaSunshine/KeywordExtraction',
    license='',
    author=' Zididada Sunshine',
    install_requires=['gensim',
                      'beautifulsoup4',
                      'numpy',
                      'nltk',
                      'contractions'],
    author_email='',
    description=''
)