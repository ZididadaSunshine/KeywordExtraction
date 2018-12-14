import unittest
from KeywordExtraction.preprocessing.text_preprocessing import *


class PreprocessingTestCase(unittest.TestCase):

    def test_replace_contractions(self):
        string = "Please don't preprocess this text."
        res = replace_contractions(string)
        self.assertEqual(res, "Please do not preprocess this text.")

    def test_strip_html(self):
        string = "This string has <div>HTML<div> in it."
        res = strip_html(string)
        self.assertEqual(res, "This string has HTML in it.")

    def test_cleanup_text(self):
        string = "This string doesn't have contractions and no <div>HTML<div> in it."
        res = cleanup_text(string)
        self.assertEqual(res, "This string does not have contractions and no HTML in it.")

    def test_normalize_numbers_in_words(self):
        string = "this string has a W0RD with some numb3rs in it that should be removed"
        expected = "this string has a with some in it that should be removed".split(' ')
        res = normalize(string.split(' '))
        self.assertListEqual(res, expected)

    def test_negate_words(self):
        string = "this sentence does not have negated words".split(' ')
        expected = "this sentence does not have_NEG negated_NEG words_NEG".split(' ')
        res = negate_words(string)
        self.assertListEqual(res, expected)

    def test_negate_words_with_punctuation(self):
        string = "this sentence does not have negated words . also these words".split(' ')
        expected = "this sentence does not have_NEG negated_NEG words_NEG . also these words".split(' ')
        res = negate_words(string)
        self.assertListEqual(res, expected)

    def test_remove_punctuation(self):
        string = "this sentence has punctuation . in , it".split(' ')
        expected = "this sentence has punctuation in it".split(' ')
        res = remove_punctuation(string)
        self.assertListEqual(res, expected)

    def test_remove_stopwords(self):
        string = "this sentence has stopwords and stopwords for me".split(' ')
        expected = "sentence stopwords stopwords".split(' ')
        res = remove_stopwords(string)
        self.assertListEqual(res, expected)

    def test_lemmatize_verbs(self):
        string = "this sentence proceeds to surprises".split(' ')
        expected = "this sentence proceed to surprise".split(' ')
        res = lemmatize_verbs(string)
        self.assertListEqual(res, expected)

    def test_get_processed_text(self):
        string = "This is a test text . It contains some <div>HTML<div> , some punctuation , doesn't have contractions , and some."
        expected = "test text contain html punctuation have_NEG contractions_NEG and_NEG".split(' ')
        res = get_processed_text(string, no_stopwords=True, lemmatize=True, negate=True)
        self.assertListEqual(res, expected)

if __name__ == '__main__':
    unittest.main()