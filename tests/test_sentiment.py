import unittest
from scripts.sentiment import *


class TestGetSentimentFunctions(unittest.TestCase):

    def test_sentiment_text(self):
        text = 'My name is John'
        text_sentiment = sentiment_text(text)
        self.assertEqual(text_sentiment, 0.0)

    def test_sentiment_empty_text(self):
        text = ''
        text_sentiment = sentiment_text(text)
        self.assertEqual(text_sentiment, 0.0)

    def test_sentiment_sentences(self):
        text = 'My name is John. What is your name?'
        sentence_sentiment = sentiment_text_sentences(text)
        self.assertEqual(sentence_sentiment['My name is John.'], [0.0])
        self.assertEqual(sentence_sentiment['What is your name?'], [0.0])

