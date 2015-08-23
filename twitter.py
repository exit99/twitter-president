from flask import current_app
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class StdOutListener(StreamListener):
    def __init__(self, on_data_func):
        self.on_data_func = on_data_func
        return super(StdOutListener, self).__init__()

    def on_data(self, data):
        """Continues grabbing tweets as long as this returns True."""
        self.on_data_func(data)
        return True

    def on_error(self, status):
        print status


class TwitterThreadController(object):
    def __init__(self, *args, **kwargs):
        self.threads = {}
        config = current_app.config
        self.access_token = config['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = config['TWITTER_ACCESS_TOKEN_SECRET']
        self.consumer_key = config['TWITTER_CONSUMER_KEY']
        self.consumer_secret = config['TWITTER_CONSUMER_KEY_SECRET']
        return super(TwitterThreadController, self).__init__(*args, **kwargs)

    def start_thread(self, keyword, func):
        """Starts thread and stores them on the class."""
        assert keyword not in self.threads
        # TODO: This func needs to take an argument (the keyword) when it
        # starts.
        thread = Thread(target=func)
        thread.start()
        self.thread[keyword] = thread

    def create_tweets(self, keywords):
        """Returns a list of tweets for the given keywords."""
        stream = self.connect_to_twitter()
        stream.filter(track=keywords)
        return l.filtered_tweets

    def connect_to_twitter(self)
        """Handles Twitter authetication and the Streaming API connection."""
        l = StdOutListener(self._on_data_func)
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        stream = Stream(auth, l)
        return stream

    def _on_data_func(self, data):
        socketio.emit('message', {'broadcast': True})
        return data



