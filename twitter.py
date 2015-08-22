import json

# Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


# Variables that contains the user credentials to access Twitter API
access_token = "154999421-iJ1K3B0g3RbsVoLf0uwy2hrhb5MdJGhpj6aU2FqV"
access_token_secret = "bfo25pn6ZVB7tKldc0CDNRqaxKVk7m0Pam6hSYzi7DSYB"
consumer_key = "I65i99rig1qoilMrVnzthm7UB"
consumer_secret = "2Kv2ZGptBMuD9dKsp7QNsOYKI5B69m7tt4myFzURilLDZQND0g"


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def on_data(self, data):
        """Continues grabbing tweets as long as this returns True."""
        # Do stuff with it here
        return True

    def on_error(self, status):
        print status


def create_tweets(keywords):
    """Returns a list of tweets for the given keywors

    :param keywords: A list of keywords to search for.
    """
    # This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    # This line filter Twitter Streams to capture data by the keywords: "Obama"
    stream.filter(track=keywords)
    return l.filtered_tweets
