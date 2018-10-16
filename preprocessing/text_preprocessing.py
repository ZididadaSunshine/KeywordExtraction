
from itertools import islice

def read_stopwords(from_file = 'stopwords.txt'):
    ''' Read stopwords (space separated) from a file and return as a list of strings. '''
    try:
        fp = open(from_file)
        words = fp.read().split(' ')
        fp.close()
        return words
    except FileNotFoundError as err: 
        print(f'Could not find file: {from_file}.')
        print(f'Full exception:')
        print(err)
        exit(-1)

def get_attribute_vector(tokenized_text, token_set):
    ''' Converts a list of tokens to a vector of {token : attributes} forms. '''
    if len(token_set) == 0: 
        raise Exception('Cannot convert a text to attribute vector without a token set.')

   

def remove_punctuation(text):
    ret = '' 
    for char in text: 
        if char.isalpha() or char == ' ':
            ret += char 

    return ret


def tokenize(text, stopwords, only_letters = True):
    ''' Convert a text to a list of tokens.
        Omits all words in the stopwords parameter.
        Removes all characters that are punctuation chars 
        if only_letters is True.
    '''

    text = text.lower()

    if only_letters: 
        text = remove_punctuation(text)

    words = text.split(' ')
    return [word for word in words if (word not in stopwords)]

def get_cooccurence_matrix(tokenized_text, tokens):
    tokens = list(tokens)
    # 2-d matrix where ["some"]["string"] yield the cooccurrence of "some" and "string"
    matrix = [[0 for token in tokens] for token in tokens] 
    token_indexes = {token : tokens.index(token) for token in tokenized_text}
    
    sentences = [ tokenized_text[i:i + 2] for i in range(len(tokenized_text) - 1)]
    for sentence in sentences: 
        idx1 = token_indexes[sentence[0]]
        idx2 = token_indexes[sentence[1]]
        matrix[idx1][idx2] += 1

    return matrix, token_indexes


def preprocess_corpus(corpus, stopwords):
    tokens = set()
    tokenized_texts = []

    for text in corpus: 
        # Gather all the tokens in the corpus
        tokenized_text = tokenize(text, stopwords)
        tokens.union(set(tokenized_text))
    
    return [get_attribute_vector(tokenized_text, tokens) for tokenized_text in tokenized_texts]


test()