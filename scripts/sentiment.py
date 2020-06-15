from textblob import TextBlob
import collections
import logging
import time

# Log transport
logging.basicConfig(level=logging.INFO)


def sentiment_text(text):
    text = text.lstrip().rstrip()
    analyze_text = TextBlob(text)
    logging.info('Sentiment of whole text: {}'.format(analyze_text.sentiment.polarity))
    time.sleep(.8)
    return analyze_text.sentiment.polarity


def sentiment_text_sentences(text):
    text = text.lstrip().rstrip()
    sentiment_dict = collections.defaultdict(list)
    analyze_text = TextBlob(text)

    # Get sentiment of each sentence.
    for sentence in analyze_text.sentences:
        sentiment_dict[sentence].append(sentence.sentiment.polarity)

    return sentiment_dict
