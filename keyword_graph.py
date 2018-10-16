import networkx as nx 
from preprocessing import text_preprocessing as tp

class TKGExtractor():

    def __init__(self, corpus):
        ''' Initializes a TKGExtractor object that is able to build 
            a word graph over a corpus (list of texts as strings) of texts 
            and extract keywords from the graph. 
        '''
        self.tokenize_corpus(corpus)
         

    def tokenize_corpus(self, corpus):
        stopwords = tp.read_stopwords(from_file = 'preprocessing/STOPWORDS.txt')
        self.attribute_vectors = tp.preprocess_corpus(corpus, stopwords = stopwords)

    def build_graph(self):
        graph = nx.Graph()
        vector = self.attribute_vectors[0]
        for word, count in vector: 
            graph.add_node(word)



    