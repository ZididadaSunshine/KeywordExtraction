import networkx as nx 
import operator
from preprocessing import text_preprocessing as tp
from collections import Counter
import nltk

class TKGExtractor():

    def __init__(self, corpus):
        ''' Initializes a TKGExtractor object that is able to build 
            a word graph over a corpus (list of texts as strings) of texts 
            and extract keywords from the graph. 
        '''
        self.tokenize_corpus(corpus)
         

    def tokenize_corpus(self, corpus):
        stopwords = open('preprocessing/stopwords.txt').read().split(' ')
        token_streams, token_set = tp.tokenize_corpus(corpus, stopwords)
        self.token_streams = token_streams
        self.token_set = token_set

    def build_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.token_set)

        for token_stream in self.token_streams: 
            # Create shingles for conducting all-neighbour-edging
            shingles = [token_stream[i : i + 5] for i  in range(0, len(token_stream) - 4)]

            # Conducting 3-neighbour-edging. For every token, we add
            # an edge between it and each the 3 following words.
            # Equal weighting, so all edges have the same weight. 
            for shingle in shingles: 
                first_token = shingle[0]
                for neighbour in shingle[1:]:
                    graph.add_edge(first_token, neighbour)

        return graph

    def extract_n_keywords(self, n = 5):
        graph = self.build_graph()
        closeness_scores = nx.closeness_centrality(graph)
        closeness_scores = sorted(closeness_scores.items(), key=operator.itemgetter(1))
        closeness_scores.reverse()
        return [word for (word, closeness) in closeness_scores[:n]]
                




# ------ DEMO ------ #        

corpus = open('preprocessing/test.txt').readlines()

extractor = TKGExtractor(corpus)
keywords = extractor.extract_n_keywords(n = 15)
print(keywords)