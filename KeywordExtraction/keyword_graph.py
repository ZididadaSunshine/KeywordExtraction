import networkx as nx 
import operator
from KeywordExtraction.preprocessing.text_preprocessing import get_processed_text


class TKGExtractor():
    def __init__(self, corpus):
        ''' Initializes a TKGExtractor object that is able to build 
            a word graph over a corpus (list of texts as strings) of texts 
            and extract keywords from the graph. 
        '''
        print(f'--------- INITIALIZING KEYWORD EXTRACTION -----------')
        t_stream, t_all = self.tokenize_corpus(corpus)
        print(f'TKGExtractor instance created with the following corpus properties: ')
        print(f'    - Number of documents: {len(corpus)}')
        num_words = [len(post) for post in corpus]
        sum_words = sum(num_words)
        print(f'    - Total words: {sum_words}')
        avg_words = sum_words / len(corpus)
        print(f'    - Avg. post length: {avg_words}')
        print(f'    - Number of unique words: {len(t_all)}')
        
    def _tokenize_corpus(self, corpus): 
        print(f'Tokenizing...')
        token_streams = [get_processed_text(text, lemmatize=True) for text in corpus]
        print(f'Preprocessing completed, received token streams.')
        tokens_all = set()
        for token_stream in token_streams: 
            tokens_all.update(set(token_stream))
        return token_streams, tokens_all

    def tokenize_corpus(self, corpus):
        
        token_streams, token_set = self._tokenize_corpus(corpus)
        self.token_streams = token_streams
        self.token_set = token_set

    def build_graph(self):
        print(f'Building graph...')
        graph = nx.Graph()
        graph.add_nodes_from(self.token_set)
        print(f'Added {len(self.token_set)} nodes to graph...')

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

        print(f'Added {len(graph.edges())} edges between nodes to graph...')

        return graph

    def extract_n_keywords(self, n = 5):
        print(f'Extracting {n} keywords...')
        graph = self.build_graph()
        print(f'Graph building completed.')
        closeness_scores = nx.closeness_centrality(graph)
        print(f'Completed closeness centrality...')
        closeness_scores = sorted(closeness_scores.items(), key=operator.itemgetter(1))
        print(f'Sorted closeness scores...')
        closeness_scores.reverse()
        print(f'Returning keywords...')
        return [word for (word, closeness) in closeness_scores[:n]]
