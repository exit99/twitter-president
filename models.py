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

    def update_sentiment_score(self, state, score):
        ts = TweetSentiment.get_or_create(candidate=self, state=state)
        ts.update_score(score)
        ts.publish()

    @classmethod
    def subscribe(cls):
        pubsub = redis.pubsub()
        pubsub.subscribe(cls.channel)
        while True:
            for item in pubsub.listen():
                data = item.get('data')
                if isinstance(data, str):
                    pk = data.split('-')[-1]
                    sentiment = session.query(TweetSentiment).get(int(pk))
                    if sentiment:
                        socketio.emit(cls.msg_name, sentiment.map_data,
                                      namespace=cls.namespace)

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

    def publish(self):
        msg = "{}-{}".format(self.__class__.__name__, self.pk)
        redis.publish(self.channel, msg)

    @property
    def sentiment(self):
        return self._sentiment / self.total_tweets

    @property
    def map_data(self):
        return {
            "name": self.candidate.name,
            "state": self.state.value,
            "sentiment": self.sentiment * 100.0,
            "total_tweets": self.total_tweets,
        }

    def __repr__(self):
        return "<TweetSentiment '{}': '{}'>".format(self.candidate.name,
                                                    self.state)
