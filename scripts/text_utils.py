# Utility functions
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import sent_tokenize, word_tokenize
import collections
import inflect
import contractions
import re
import unicodedata


def replace_contractions(text):
    """Replace contractions in string of text"""
    return contractions.fix(text)


def remove_non_ascii(words):
    """Remove non-ASCII characters"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words


def to_lowercase(words):
    """Convert all characters to lowercase"""
    return [_.lower() for _ in words]


def remove_punctuation(words):
    """Remove punctuation"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words


def replace_numbers(words):
    """Replace all integer occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words


def remove_stopwords(words):
    """Remove stop words"""
    return [_ for _ in words if _ not in stopwords.words('english')]


def stem_words(words):
    """Stem words"""
    stemmer = LancasterStemmer()
    return [stemmer.stem(word) for word in words]


def lemmatize_verbs(words):
    """Lemmatize verbs"""
    lemmatizer = WordNetLemmatizer()
    return [lemmatizer.lemmatize(word, pos='v') for word in words]


def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    # words = replace_numbers(words)
    words = remove_stopwords(words)

    return words


def stem_and_lemmatize(words):
    words = normalize(words)
    stems = stem_words(words)
    lemmas = lemmatize_verbs(words)
    return stems, lemmas


def process_text(text):
    """Returns word and sentence tokens and sentences"""
    text = replace_contractions(text)

    tokens = word_tokenize(text)
    sentences = sent_tokenize(text)

    # Process word tokens. Get lemmas
    _, word_tokens = stem_and_lemmatize(tokens)

    # For each sentence token, feed sentence to lemma pipeline and store in a dict
    sentences_tokens = []
    for sent in sentences:
        sent = sent.split()
        _, sent_token = stem_and_lemmatize(sent)
        sentences_tokens.append(sent_token)

    return word_tokens, sentences_tokens, sentences


def count_words(tokens):
    """Count words"""
    word_counts = collections.defaultdict(int)
    for token in tokens:
        word_counts[token] += 1
    return word_counts


def word_freq_distribution(word_counts):
    """Word frequency distribution"""
    freq_dist = {}
    max_freq = max(word_counts.values())
    for word in word_counts.keys():
        freq_dist[word] = (word_counts[word] / max_freq)

    return freq_dist


def score_sentences(sentences, sentences_tokens, freq_dist):
    """Score sentences by frequency distribution.
    max_len = maximum length to sentences which are to be considered
    """
    sent_scores = collections.defaultdict(float)
    keys = set(freq_dist.keys())

    for index, sent in enumerate(sentences):
        for word in sentences_tokens[index]:
            if word in keys:
                sent_scores[index, sent] += freq_dist[word]

    return sent_scores
