import nltk 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer


def setup():
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')


def get_stopwords():
    return open('./app/preprocessing/STOPWORDS.txt').read().split(' ')


def tokenize(text, stopwords):
    res = ''

    # Remove punctuation
    for char in text:
        if char.isalpha() or char == ' ':
            res += char
    # Lemmatizing instead of stemming because it looks better.

    lemmatizer = WordNetLemmatizer()
    token_stream = res.lower()
    token_stream = token_stream.split(' ')
    token_stream = [lemmatizer.lemmatize(word) for word in token_stream if word not in stopwords and not word == '']
    shingles = zip(token_stream[1:], token_stream[2:])
    token_stream = []
    for first, second in shingles:
        if is_valid_phrase(first, second):
            token_stream.append(f'{first} {second}')
        else:
            token_stream.append(first)

    return token_stream


def tokenize_corpus(corpus, stopwords):
    token_streams = [tokenize(document, stopwords) for document in corpus]
    token_set = set([token for token_stream in token_streams for token in token_stream])
    return token_streams, token_set


def is_valid_phrase(x, y):
    # Allowed combinations:
    # - RB, JJ  -> Adverb describing a adjective, e.g. "completely shitty"
    # - JJ, NN  -> Adjective describing a noun, e.g. "great service"
    tagged_words = nltk.pos_tag([x, y])
    (_, tag1) = tagged_words[0]
    (_, tag2) = tagged_words[1]
    return (tag1 == 'RB' and tag2 == 'JJ') or (tag1 == 'JJ' and tag2 == 'NN')
