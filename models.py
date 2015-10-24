import re

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types.choice import ChoiceType

import config
from constants import STATES
from extensions import Base, session, redis, socketio
from mixins import ModelMixin


class _SocketMixin():
    channel = config.SENTIMENT_REDIS_CHANNEL
    msg_name = config.PRESIDENTIAL_SOCKETIO_MSG_NAME
    namespace = config.PRESIDENTIAL_SOCKETIO_NAMESPACE


class PresidentialCandidate(_SocketMixin, ModelMixin, Base):
    __tablename__ = "presidential_candidate"
    pk = Column(Integer, primary_key=True)
    name = Column(String(120))

    def update_sentiment_score(self, state, score, msg=None):
        ts = TweetSentiment.get_or_create(candidate=self, state=state)
        ts.update_score(score)
        return ts

    def publish(self, sentiment, msg=""):
        sentiment.publish(msg)

    @classmethod
    def subscribe(cls):
        pubsub = redis.pubsub()
        pubsub.subscribe(cls.channel)
        while True:
            for item in pubsub.listen():
                data = item.get('data')
                if isinstance(data, str):
                    limter = len(re.findall('.*?-.*?-.*?-.*?-', data)[0])
                    tweet_info = data[:limter - 1].split('-')
                    name, state, sentiment, total_tweets = tweet_info
                    msg = data[limter:]
                    data = {
                        'name': name,
                        'state': state,
                        'sentiment': sentiment,
                        'total_tweets': total_tweets,
                        'msg': msg
                    }
                    socketio.emit(cls.msg_name, data, namespace=cls.namespace)

    @classmethod
    def current_map_data(cls):
        data = {}
        for candidate in session.query(cls).all():
            data[candidate.name] = {}
            q = session.query(TweetSentiment)
            sentiments = q.filter_by(candidate=candidate)
            for sentiment in sentiments.all():
                map_data = sentiment.map_data
                data[map_data.pop('name')][map_data.pop('state')] = map_data
        return data

    def __repr__(self):
        return "<PresidentialCandidate '{}'>".format(self.name)


class TweetSentiment(_SocketMixin, ModelMixin, Base):
    __tablename__ = "candidate_tweet_sentiment"
    pk = Column(Integer, primary_key=True)
    _sentiment = Column(Float, default=0.0)
    total_tweets = Column(Integer, default=0)
    state = Column(ChoiceType([(abbr, abbr) for abbr in STATES.values()]))
    _candidate_pk = Column('candidate_pk', Integer,
                           ForeignKey(PresidentialCandidate.pk))

    candidate = relationship(
        'PresidentialCandidate',
        backref=backref('sentiments', lazy='dynamic')
    )

    def update_score(self, score):
        self.total_tweets += 1
        self._sentiment = self._sentiment + score
        session.add(self)
        session.commit()

    def publish(self, tweet_msg=""):
        msg = "{}-{}-{}-{}-{}".format(
            self.candidate.name,
            self.state.value,
            self.sentiment,
            self.total_tweets,
            tweet_msg.encode('utf-8', "ignore"),
        )
        redis.publish(self.channel, msg)

    @property
    def sentiment(self):
        return (self._sentiment / self.total_tweets) * 100

    @property
    def map_data(self):
        return {
            "name": self.candidate.name,
            "state": self.state.value,
            "sentiment": self.sentiment,
            "total_tweets": self.total_tweets,
        }

    def __repr__(self):
        return "<TweetSentiment '{}': '{}'>".format(self.candidate.name,
                                                    self.state)
