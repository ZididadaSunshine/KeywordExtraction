
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
    ''' Converts a list of tokens to a vector of {token : count} forms. '''
    if len(token_set) == 0: 
        raise Exception('Cannot convert a text to attribute vector without a token set.')

    att_vector = {token : 0 for token in token_set}
    for token in tokenized_text:
        att_vector[token] += 1

    return att_vector


def tokenize(text, special_character_mapping = {}):
    ''' Convert a text to a list of tokens.
        Any tokens found in the special_character_mapping will take 
        the mapped form. All other tokens are tokenized as is. 
    '''
    words = text.split(' ')
    return [special_character_mapping[word] 
            if word in special_character_mapping 
            else word 
            for word in words]


