from nltk.tokenize import sent_tokenize, word_tokenize
from scripts.text_utils import process_text, count_words, word_freq_distribution, score_sentences
import collections
import heapq


def generate_summary(text, k):
    """Returns top k sentences to represent the summary of the article"""

    # Generate word and sentence tokens
    word_tokens, sentences_tokens, sentences = process_text(text)
    if not word_tokens or not sentences:
        return 'Something went wrong. Please try again.'

    # Count words
    word_counts = count_words(word_tokens)
    # Word frequency distribution
    freq_dist = word_freq_distribution(word_counts)
    # Score sentences by using the frequency distribution
    sent_scores = score_sentences(sentences, sentences_tokens, freq_dist)
    top_sents = collections.Counter(sent_scores)
    # Get top k sentences by sentence scores
    top = top_sents.most_common(k)
    # Heapify such that top k sentences are ordered by sentence index
    top = [list(_[0]) for _ in top]
    heapq.heapify(top)

    summary = ''
    for t in top:
        # Capitalize first character
        summary += t[1][0].upper() + t[1][1:] + ' '

    return summary[:-1]
