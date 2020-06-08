from textblob import TextBlob
import collections
import logging

# Log transport
logging.basicConfig(level=logging.INFO)


def sentiment_text(text):
    analyze_text = TextBlob(text)
    logging.info('Input text: {}'.format(text))
    logging.info('Sentiment: {}'.format(analyze_text.sentiment.polarity))
    return analyze_text.sentiment.polarity


def sentiment_text_sentences(text):
    sentiment_dict = collections.defaultdict(list)
    analyze_text = TextBlob(text)

    # Get sentiment of each sentence.
    for sentence in analyze_text.sentences:
        sentiment_dict[sentence].append(sentence.sentiment.polarity)

    return sentiment_dict
