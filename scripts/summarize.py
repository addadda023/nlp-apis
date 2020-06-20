from nltk.tokenize import sent_tokenize, word_tokenize
from scripts.text_utils import process_text, count_words, word_freq_distribution, score_sentences
import collections
import time


def generate_summary(text, k=5):
    """Returns top k sentences to represent the summary of the article"""

    # Generate word and sentence tokens
    tokens, sents = process_text(text)
    if not tokens or not sents:
        return 'Something went wrong. Please try again.'
    # Count words
    word_counts = count_words(tokens)
    # Word frequency distribution
    freq_dist = word_freq_distribution(word_counts)
    # Score sentences by using the frequency distribution
    sent_scores = score_sentences(sents, freq_dist, max_len=40)

    top_sents = collections.Counter(sent_scores)
    summary = ''
    top = top_sents.most_common(k)
    for t in top:
        # Capitalize first character
        t = t[0].strip()
        t = t[0].upper() + t[1:]
        summary += t + '. '

    time.sleep(1)
    return summary[:-1]