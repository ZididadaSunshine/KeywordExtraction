import unittest
from KeywordExtraction.keyword_graph import *


class KeywordGraphTest(unittest.TestCase):

    def setUp(self):
        str1 = "This is a text that should be split into several lower case tokens"
        str2 = "this is also a text that should be split"
        self.corpus = [str1, str2]
        self.kwe = TKGExtractor(self.corpus)

    def edge_equals(self, first, second):
        f1, f2 = first
        s1, s2 = second
        return (f1 == s1 and f2 == s2) or (f1 == s2 and f2 == s1)

    def test_proper_token_streams(self):
        self.assertEqual(len(self.kwe.token_streams), len(self.corpus))

    def test_non_empty_token_streams(self):
        self.assertTrue(len(self.kwe.token_streams[0]) > 0)
        self.assertTrue(len(self.kwe.token_streams[1]) > 0)

    def test_token_set(self):
        token_set = {'split', 'several', 'case', 'text', 'tokens', 'also', 'lower'}
        self.assertSetEqual(self.kwe.token_set, token_set)

    def test_tokenize_corpus(self):
        expected_token_set = {'split', 'several', 'case', 'text', 'tokens', 'also', 'lower'}
        self.kwe.tokenize_corpus(self.corpus)
        streams = self.kwe.token_streams
        tokens = self.kwe.token_set
        self.assertSetEqual(expected_token_set, tokens)
        self.assertTrue(len(streams[0]) > 0)
        self.assertTrue(len(streams[1]) > 0)

    def test_tokenize_corpus_private(self):
        expected_token_set = {'split', 'several', 'case', 'text', 'tokens', 'also', 'lower'}
        streams, tokens = self.kwe._tokenize_corpus(self.corpus)
        self.assertSetEqual(expected_token_set, tokens)
        self.assertTrue(len(streams[0]) > 0)
        self.assertTrue(len(streams[1]) > 0)

    def test_build_graph(self):
        graph = self.kwe.build_graph()
        nodes = [node for node in graph.nodes()]
        edges = [edge for edge in graph.edges()]
        expected_nodes = self.kwe.token_set
        # Edges generated from 4-neighbour edging
        expected_edges = [('text', 'lower'), ('text', 'case'), ('tokens', 'split'), ('text', 'split'),
                          ('several', 'split'), ('several', 'text'), ('case', 'split'), ('lower', 'split')]
        for edge in edges:
            found = False
            for expected_edge in expected_edges:
                if self.edge_equals(edge, expected_edge):
                    found = True
            self.assertTrue(found)

        self.assertSetEqual(set(nodes), set(expected_nodes))

    def test_extract_keywords_keywords_from_tokens(self):
        keywords = self.kwe.extract_n_keywords()
        self.assertTrue(len(keywords) > 0)
        for word in keywords:
            self.assertTrue(word in self.kwe.token_set)


if __name__ == '__main__':
    unittest.main()