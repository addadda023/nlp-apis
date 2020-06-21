import unittest
from scripts.text_utils import *


class TestTextUtils(unittest.TestCase):

    def test_replace_contractions(self):
        contracted_text = "you've"
        self.assertEqual(replace_contractions(contracted_text), 'you have')

    def test_remove_non_ascii(self):
        text_with_ascii = '6Â 918Â 417Â 712'
        self.assertEqual(remove_non_ascii(text_with_ascii.split()), ['6A', '918A', '417A', '712'])