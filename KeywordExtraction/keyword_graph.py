import networkx as nx 
import operator
from KeywordExtraction.preprocessing.text_preprocessing import get_processed_text
import nltk

class TKGExtractor():
    def __init__(self, corpus):
        ''' Initializes a TKGExtractor object that is able to build 
            a word graph over a corpus (list of texts as strings) of texts 
            and extract keywords from the graph. 
        '''
        self.tokenize_corpus(corpus)
        num_words = [len(post) for post in corpus]
        sum_words = sum(num_words)
        avg_words = sum_words / len(corpus)
        
    def _tokenize_corpus(self, corpus):
        token_streams = [get_processed_text(text, lemmatize=True, no_stopwords=True) for text in corpus]
        tokens_all = set()
        for token_stream in token_streams: 
            tokens_all.update(set(token_stream))

        return token_streams, tokens_all

    def tokenize_corpus(self, corpus):
        token_streams, token_set = self._tokenize_corpus(corpus)

        self.token_streams = token_streams
        self.token_set = token_set

    def build_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.token_set)

        for token_stream in self.token_streams: 
            # Create shingles for conducting all-neighbour-edging
            shingles = [token_stream[i : i + 5] for i  in range(0, len(token_stream) - 4)]

            # Conducting 4-neighbour-edging. For every token, we add
            # an edge between it and each the 3 following words.
            # Equal weighting, so all edges have the same weight. 
            for shingle in shingles: 
                first_token = shingle[0]
                for neighbour in shingle[1:]:
                    graph.add_edge(first_token, neighbour)

        return graph

    def extract_n_keywords(self, n=10):
        graph = self.build_graph()
        closeness_scores = nx.pagerank(graph)
        closeness_scores = sorted(closeness_scores.items(), key=operator.itemgetter(1))
        closeness_scores.reverse()
        words = [word for word, score in closeness_scores]
        return words[:n]

