import networkx as nx 
import operator
from preprocessing import text_preprocessing as tp
from collections import Counter

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
            # Define shingles 
            shingles = [token_stream[i : i + 2] for i in range(len(token_stream) - 1)]

            # Nearest Neighbour Edging
            # For every shingle, add to the weight between the co-occurrent words
            # Add the edge if it doesn't already exist
            for shingle in shingles:
                first, second = shingle[0], shingle[1]
                edge_data = graph.get_edge_data(first, second)
                if edge_data == None: 
                    # Doesn't exist, add it with weight = 1
                    graph.add_edge(first, second, weight = 1)
                else: 
                    # Increase the weight 
                    graph.add_edge(first, second, weight = edge_data['weight'] + 1)
            
            for u, v in graph.edges(): 
                # Invert weights to shortest path works appropriately when words co-occur
                edge = graph.get_edge_data(u ,v)
                graph.add_edge(u, v, weight = 1 / edge['weight'])

        return graph
                




# ------ DEMO ------ #        

corpus = open('preprocessing/test.txt').readlines()
ext = TKGExtractor(corpus)
graph = ext.build_graph()

# Degree centrality
degree_centrality = sorted(graph.degree, key = lambda x: x[1], reverse=True)
print(f'According to degree centrality, the 5 most common words are: {[word for word, count in degree_centrality[:5]]}')

# Closeness centrality 
# Sum the shortest paths to all other nodes 
nodes = graph.nodes()
nodes_with_closeness = {}

shortest_paths = nx.shortest_path(graph, weight = 'weight')
for key, value in shortest_paths.items():
    # Key is the word, value is a dictionary of WORD -> PATH_TO_WORD_FROM_KEY. 
    # Sum the path lengths, take the inverse, add to key word 
    nodes_with_closeness[key] = 1 / sum(len(path) for node, path in value.items())

closeness_centrality = sorted(nodes_with_closeness.items(), key = operator.itemgetter(1), reverse = True)
print(f'According to closeness centrality, the 5 most common words are: {[word for word, count in closeness_centrality[:5]]}')

