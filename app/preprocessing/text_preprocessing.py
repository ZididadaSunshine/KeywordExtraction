# Required installs: 
# - pip3 install contractions
# - pip3 install nltk 
# - - nltk.download("wordnet")
# - - nltk.download("averaged_perceptron_tagger")
# - pip3 install beautifulsoup

import re, string, unicodedata
import nltk
import contractions
from bs4 import BeautifulSoup
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import json 
from gensim.models import KeyedVectors
from gensim.test.utils import datapath
import numpy as np
import pandas as pd 

def adjust_contractions_dict(): 
    to_add = {}
    for key, value in contractions.contractions_dict.items(): 
        if "I" in key: 
            to_add[key.lower()] = value 

    for key, value in to_add.items(): 
        contractions.contractions_dict[key] = value.lower()

def setup():
    nltk.download('wordnet')
    nltk.download('averaged_perceptron_tagger')


def get_stopwords():
    return open('./app/preprocessing/STOPWORDS.txt').read().split(' ')

def is_valid_phrase(x, y):
    # Allowed combinations:
    # - RB, JJ  -> Adverb describing a adjective, e.g. "completely shitty"
    # - JJ, NN  -> Adjective describing a noun, e.g. "great service"
    tagged_words = nltk.pos_tag([x, y])
    (_, tag1) = tagged_words[0]
    (_, tag2) = tagged_words[1]
    return (tag1 == 'RB' and tag2 == 'JJ') or (tag1 == 'JJ' and tag2 == 'NN')


# --- Text cleanup --- #
def strip_html(text):
    soup = BeautifulSoup(text, "html.parser")
    return soup.get_text()

def replace_contractions(text):
    return contractions.fix(text)

def cleanup_text(text):
    text = re.sub(r'(@[A-Za-z0-9]+)|(\w+:\/\/\S+)','', text) # Remove Twitter handles, tags
    text = strip_html(text)
    text = replace_contractions(text)
    return text

# --- Text normalization --- # 
def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words

def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    return [word.lower() for word in words]

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '' and new_word != "_NEG":
            new_words.append(new_word)
    return new_words

def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    return [word for word in words if word not in stopwords.words('english')]

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = SnowballStemmer(language = 'english')
    return [stemmer.stem(word) for word in words]

def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    lemmas = []
    return [lemmatizer.lemmatize(word, pos='v') for word in words]

def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    return words

# --- Post-normalization processing --- #
def is_negation(word): 
    return re.match(r"""
            never|no|nothing|nowhere|noone|
            none|not|havent|hasnt|hadnt|
            cant|couldnt|shouldnt|wont|
            wouldnt|dont|doesnt|didnt|
            isnt|arent|aint|
            n't
            """, word)

def is_punctuation(word): 
    return re.match(r'\.|:|;|!|\?', word)

def negate_words(text): 
    """ Appends "_NEG" to all words following a negating word until a punctuation mark is met. """
    result = []
    do_negate = False

    for word in text: 
        # Check if the negation state should be changed
        if is_negation(word):
            do_negate = True 
            result.append(word)
        elif is_punctuation(word): 
            do_negate = False
            result.append(word)
        else: 
            if do_negate: 
                result.append(f'{word}_NEG')
            else: 
                result.append(word) 
    
    return result

def words_to_word2vec(words, word2vec_model): 
    result = []
    for word in words: 
        try: 
            if '_NEG' in word: 
                result.append( np.append(word2vec_model[word.replace('_NEG', '')], [1]) )
            else: 
                result.append( np.append(word2vec_model[word], [0]) )
        except: 
            continue

    return result
        

def get_processed_text(text, negate = False, stem = False, lemmatize = False, as_word2vec = False): 
    """ 
    Returns a list of tokens after processing the text by: 
    1. Removing HTML and Twitter handles
    2. Tokenizing words
    3. Normalizing words (lowercase, removing non-ASCII)
    4. Negating words following a negation if so chosen
    5. Removing stopwords
    6. Removing punctutation
    7. Stemming or lemmatizing if so chosen
    
    If as_word2vec is set to True, returns a list of 301-d vectors (the last element is 1 if the word is negated, 0 otherwise). """
    adjust_contractions_dict()
    word2vec = None 
    if as_word2vec: 
        # Requires that the word2vec.bin file is in the gensim subdiretory of the Python directory.
        print('Loading word2vec...')
        word2vec = KeyedVectors.load_word2vec_format(datapath('word2vec.bin'), binary = True)

    text = cleanup_text(text)
    words = word_tokenize(text)
    words = normalize(words)
    if negate: 
        words = negate_words(words)
    words = remove_stopwords(words)
    words = remove_punctuation(words)
    if stem: 
        words = stem_words(words)
    if lemmatize: 
        words = lemmatize_verbs(words)
    if as_word2vec: 
        words = words_to_word2vec(words, word2vec)

    return words


# TEST 