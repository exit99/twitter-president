import json
import sys
import threading
if 'threading' in sys.modules:
    del sys.modules['threading']

import gevent
import gevent.socket
import gevent.monkey
gevent.monkey.patch_all()

import indicoio
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import local_settings
from constants import CANDIDATES, PARTIES, STATES
from extensions import socketio


class StdOutListener(StreamListener):
    def __init__(self, *args, **kwargs):
        self.keyword = kwargs.pop('keyword')
        return super(StdOutListener, self).__init__(self, *args, **kwargs)

    def on_error(self, status):
        print "ERRRR" * 10
        print status

    def on_data(self, data):
        """Continues grabbing tweets as long as this returns True."""
        tweet = Tweet(json.loads(data))
        if tweet.is_relevant:
            print tweet.state, tweet.sentiment_score, tweet.candidates, tweet.text
            # TODO YOU ARE HERE SENDING THE DATA TO THE CLIENT.
            # Todo save to database here.
            # socketio.emit('message', {'broadcast': True})
        return True


def start_twitter_streams(keywords):
    keyword_stream(keywords)
    thread = threading.Thread(target=keyword_stream, args=(keywords,))
    thread.start()
    return thread


def stream_api_connection(keyword):
    """Handle Twitter authetification and the connection to Streaming API."""
    access_token = local_settings.TWITTER_ACCESS_TOKEN
    access_token_secret = local_settings.TWITTER_ACCESS_TOKEN_SECRET
    consumer_key = local_settings.TWITTER_CONSUMER_KEY
    consumer_secret = local_settings.TWITTER_CONSUMER_KEY_SECRET

    l = StdOutListener(keyword=keyword)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    return stream


def keyword_stream(keywords):
    if not isinstance(keywords, list):
        keywords = [keywords]
    stream = stream_api_connection(keywords)
    stream.filter(track=keywords)


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


    @property
    def is_relevant(self):
        return self.in_usa and self.candidates

    @property
    def in_usa(self):
        return self.country_code == "US" or self.state

    @property
    def sentiment_score(self):
        return indicoio.sentiment(self.text)

    @property
    def state(self):
        if not hasattr(self, '_state'):
            user_state = None
            if self.full_name:
                user_state = self.full_name.split(', ')[-1]
            if not user_state:
                location = self.user.get('location', "").lower()
                for state, abbr in STATES.iteritems():
                    if state.lower() in location or abbr.lower() in location:
                        user_state = abbr
                        break
            self._state = user_state
        return self._state
