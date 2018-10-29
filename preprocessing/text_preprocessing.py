import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer

def tokenize(text, stopwords):
    res = '' 

    # Remove punctuation
    for char in text: 
        if char.isalpha() or char == ' ':
            res += char 

    lemmatizer = WordNetLemmatizer()
    # Stemming makes it ugly, but may be required. Not for now though.
    res = res.lower()
    token_stream = [lemmatizer.lemmatize(word) for word in res.split(' ') if word not in stopwords and not word == '']


    return token_stream


def tokenize_corpus(corpus, stopwords):
    token_streams = [tokenize(document, stopwords) for document in corpus]
    token_set = set([token for token_stream in token_streams for token in token_stream])
    return token_streams, token_set