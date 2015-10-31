import json
import logging
from datetime import datetime
from random import randint

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

import local_settings
from constants import CANDIDATES, STATES
from models import PresidentialCandidate


class Listener(StreamListener):
    def __init__(self, *args, **kwargs):
        Listener.configure_logging()
        return super(Listener, self).__init__(self, *args, **kwargs)

    def on_error(self, status):
        logging.warning('{}: Twitter API Failure - {}'.format(
            status, datetime.now()
        ))
        print "Error: {}".format(status)

    def on_data(self, data):
        """Continues grabbing tweets as long as this returns True."""
        tweet = Tweet(json.loads(data))
        if tweet.is_relevant:
            tweet.log_for_audit()
            tweet.save()
        return True

    @staticmethod
    def configure_logging():
        logging.basicConfig(filename=local_settings.LOGGING_FILE,
                            level=logging.INFO)


class Tweet(object):
    fields = (
        u'text',
        u'source',
        u'timestamp_ms',
        u'retweet_count',
        u'user',
        u'lang',
    )
    place_fields = (
        u'full_name',
        u'country',
        u'place_type',
        u'country_code',
        u'name'
    )

    def __init__(self, data):
        for field in self.fields:
            setattr(self, field, data.get(field))
        for field in self.place_fields:
            setattr(self, field, (data.get('place') or {}).get(field))
        self.candidates = [candidate for candidate in CANDIDATES
                           if candidate.lower() in self.text.lower()]
        super(Tweet, self).__init__()

    def save(self):
        for candidate in self.candidates:
            if unicode(self.state) in STATES.values():
                pc = PresidentialCandidate.get_or_create(name=candidate)
                state = unicode(self.state),
                score = self.sentiment_score
                sentiment = pc.update_sentiment_score(state, score)
                pc.publish(sentiment, self.text)

    @property
    def is_relevant(self):
        return self.in_usa and self.candidates

    @property
    def in_usa(self):
        return self.country_code == "US" or self.state

    @property
    def sentiment_score(self):
        blob = self._blob_score(self.text)
        vader = self._vader_score(self.text)
        avg = (blob + vader) / 2
        return avg

    def _blob_score(self, text):
        return (TextBlob(text).sentiment.polarity + 1.0) / 2

    def _vader_score(self, text):
        vader = vaderSentiment(text.encode('utf-8', 'ignore'))
        return (vader['pos'] - vader['neg'] + 1) / 2

    @property
    def state(self):
        if not hasattr(self, '_state'):
            user_state = None
            if self.full_name:
                user_state = self.full_name.split(', ')[-1]
            if not user_state:
                location = (self.user.get('location') or "").lower()
                for state, abbr in STATES.iteritems():
                    if state.lower() in location or abbr.lower() in location:
                        user_state = abbr
                        break
            self._state = user_state
        return self._state

    def log_for_audit(self):
        """Randomly log so we can check sentiment score is accurate."""
        if randint(0, 20) == 1:  # 5% chance.
            logging.info("{}, {}, {}".format(
                self.state, self.sentiment_score, self.candidates, self.text)
            )


def start_stream(track):
    if not isinstance(track, list):
        track = [track]
    stream = stream_api_connection()
    return stream.filter(track=track)


def stream_api_connection():
    """Handle Twitter authetification and the connection to Streaming API."""
    access_token = local_settings.TWITTER_ACCESS_TOKEN
    access_token_secret = local_settings.TWITTER_ACCESS_TOKEN_SECRET
    consumer_key = local_settings.TWITTER_CONSUMER_KEY
    consumer_secret = local_settings.TWITTER_CONSUMER_KEY_SECRET

    l = Listener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    return stream


if __name__ == "__main__":
    start_stream(CANDIDATES)
