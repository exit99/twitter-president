import json
from threading import Thread

import indicoio
from flask import current_app
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

from extensions import socketio


class StdOutListener(StreamListener):
    def __init__(self, on_data_func):
        self.on_data_func = on_data_func
        return super(StdOutListener, self).__init__()

    def on_data(self, data):
        """Continues grabbing tweets as long as this returns True."""
        self.on_data_func(json.loads(data))
        return True

    def on_error(self, status):
        print status


class TwitterThreadController(object):
    def __init__(self, *args, **kwargs):
        self.threads = {}
        self.keywords = []
        config = current_app.config
        self.access_token = config['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = config['TWITTER_ACCESS_TOKEN_SECRET']
        self.consumer_key = config['TWITTER_CONSUMER_KEY']
        self.consumer_secret = config['TWITTER_CONSUMER_KEY_SECRET']
        return super(TwitterThreadController, self).__init__(*args, **kwargs)

    def start_thread(self, keywords, func):
        """Starts thread and stores them on the class."""
        assert keywords not in self.threads
        thread = Thread(target=func, args=[keywords])
        thread.start()
        self.threads[keywords] = thread
        self.keywords.append(keywords)

    def create_tweets(self, keywords):
        """Returns a list of tweets for the given keywords."""
        stream = self.connect_to_twitter()
        stream.filter(track=keywords)

    def connect_to_twitter(self):
        """Handles Twitter authetication and the Streaming API connection."""
        l = StdOutListener(self._on_data_func)
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        stream = Stream(auth, l)
        return stream

    def _on_data_func(self, data):
        tweet = Tweet(data)
        sentiment_score, state, valid = tweet.sentiment_analysis()
        if valid:
            # TODO YOU ARE HERE SENDING THE DATA TO THE CLIENT.
            socketio.emit('message', {'broadcast': True})


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
            setattr(self, field, data.get('place', {}.get(field)))
        super(Tweet, self).__init__()

    def sentiment_analysis(self):
        if self.in_usa:
            return self.sentiment, self.state, True
        return None, None, False

    @property
    def sentiment(self):
        return (indicoio.sentiment(self.text) - 5) * self.retweet_count

    @property
    def in_usa(self):
        return self.country_code == "US"

    @property
    def state(self):
        self.full_name.split(', ')[-1]
