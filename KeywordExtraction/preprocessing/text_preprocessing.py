import re
import unicodedata

import contractions
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer


def adjust_contractions_dict():
    to_add = {}

    for key, value in contractions.contractions_dict.items():
        if "I" in key:
            to_add[key.lower()] = value

    for key, value in to_add.items():
        contractions.contractions_dict[key] = value.lower()


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
    text = strip_html(text)
    text = replace_contractions(text)
    return text


# --- Text normalization --- #
def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    result = []

    for word in words:
        word = re.sub(r'[^\w\s]', '', word)
        if word != '' and word != "_NEG":
            result.append(word)

    return result


def remove_stopwords(words):
    """Remove stopwords from list of tokenized words"""
    return [word for word in words if word not in stopwords.words('english')]


def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = SnowballStemmer(language='english')
    return [stemmer.stem(word) for word in words]


def lemmatize_verbs(words):
    """Lemmatize verbs in list of tokenized words"""
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos='v') for word in words]


def endswith_punctuation(word):
    if len(word) > 1:
        if is_punctuation(word[len(word) - 1]):
            return True

    return False


def normalize(words):
    """Remove non-ASCII characters from and lowercase tokenized words"""
    result = []

    for word in words:
        # Ignore words containing a number
        if any(char.isdigit() for char in word):
            continue

        # Ignore words with more than 2 consecutive characters
        if re.match(r'\S*((.)\2{2,})\S*', word):
            continue

        # Remove non-ASCII characters
        word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')

        # Lowercase the word
        word = word.lower()

        if endswith_punctuation(word):
            result.append(word[:len(word) - 1])
            result.append(word[len(word) - 1])
        else:
            result.append(word)

    return result


# --- Post-normalization processing --- #
def is_negation(word):
    return re.match(r'never|no|nothing|nowhere|noone|'
                    r'none|not|havent|hasnt|hadnt|'
                    r'cant|couldnt|shouldnt|wont|wouldnt|'
                    r'dont|doesnt|didnt|isnt|arent|aint|n\'t', word)


def is_punctuation(word):
    return re.match(r'[.:;!?,]', word)


def negate_words(words):
    """ Appends "_NEG" to all words following a negating word until a punctuation mark is met. """
    do_negate = False

    for i, word in enumerate(words):
        # Check if the negation state should be changed
        if is_negation(word):
            do_negate = True
        elif is_punctuation(word):
            do_negate = False
        else:
            if do_negate:
                words[i] = f'{word}_NEG'
    return words
    

def get_processed_text(text, negate=False, stem=False, no_stopwords=False, lemmatize=False):
    """ 
    Returns a list of tokens after processing the text by: 
    1. Removing HTML and Twitter handles
    2. Tokenizing words
    3. Normalizing words (lowercase, removing non-ASCII)
    4. Negating words following a negation if so chosen
    5. Removing stopwords
    6. Removing punctutation
    7. Stemming or lemmatizing if so chosen"""

    adjust_contractions_dict()

    text = cleanup_text(text)

    words = text.split()

    words = normalize(words)

    if negate:
        words = negate_words(words)

    words = remove_punctuation(words)

    if no_stopwords:
        words = remove_stopwords(words)

    if stem:
        words = stem_words(words)

    if lemmatize:
        words = lemmatize_verbs(words)

    return words
