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

    def update_sentiment_score(self, state, blob_score, *vader_scores):
        ts = TweetSentiment.get_or_create(candidate=self, state=state)
        ts.update_score(blob_score, *vader_scores)
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
    blob_score_total = Column(String(255), default="0")
    pos_vader_score_total = Column(String(255), default="0")
    neg_vader_score_total = Column(String(255), default="0")
    nuetral_vader_score_total = Column(String(255), default="0")
    compound_vader_score_total = Column(String(255), default="0")

    blob_score_range_count_0 = Column(String(255), default="0")
    pos_vader_score_range_count_0 = Column(String(255), default="0")
    neg_vader_score_range_count_0 = Column(String(255), default="0")
    nuetral_score_range_count_0 = Column(String(255), default="0")
    compound_score_range_count_0 = Column(String(255), default="0")
    blob_score_range_count_1_10 = Column(String(255), default="0")
    blob_score_range_count_11_20 = Column(String(255), default="0")
    blob_score_range_count_21_30 = Column(String(255), default="0")
    blob_score_range_count_31_40 = Column(String(255), default="0")
    blob_score_range_count_41_50 = Column(String(255), default="0")
    blob_score_range_count_51_60 = Column(String(255), default="0")
    blob_score_range_count_61_70 = Column(String(255), default="0")
    blob_score_range_count_71_80 = Column(String(255), default="0")
    blob_score_range_count_81_90 = Column(String(255), default="0")
    blob_score_range_count_91_100 = Column(String(255), default="0")
    pos_vader_score_range_count_1_10 = Column(String(255), default="0")
    pos_vader_score_range_count_11_20 = Column(String(255), default="0")
    pos_vader_score_range_count_21_30 = Column(String(255), default="0")
    pos_vader_score_range_count_31_40 = Column(String(255), default="0")
    pos_vader_score_range_count_41_50 = Column(String(255), default="0")
    pos_vader_score_range_count_51_60 = Column(String(255), default="0")
    pos_vader_score_range_count_61_70 = Column(String(255), default="0")
    pos_vader_score_range_count_71_80 = Column(String(255), default="0")
    pos_vader_score_range_count_81_90 = Column(String(255), default="0")
    pos_vader_score_range_count_91_100 = Column(String(255), default="0")
    neg_vader_score_range_count_1_10 = Column(String(255), default="0")
    neg_vader_score_range_count_11_20 = Column(String(255), default="0")
    neg_vader_score_range_count_21_30 = Column(String(255), default="0")
    neg_vader_score_range_count_31_40 = Column(String(255), default="0")
    neg_vader_score_range_count_41_50 = Column(String(255), default="0")
    neg_vader_score_range_count_51_60 = Column(String(255), default="0")
    neg_vader_score_range_count_61_70 = Column(String(255), default="0")
    neg_vader_score_range_count_71_80 = Column(String(255), default="0")
    neg_vader_score_range_count_81_90 = Column(String(255), default="0")
    neg_vader_score_range_count_91_100 = Column(String(255), default="0")
    nuetral_vader_score_range_count_1_10 = Column(String(255), default="0")
    nuetral_vader_score_range_count_11_20 = Column(String(255), default="0")
    nuetral_vader_score_range_count_21_30 = Column(String(255), default="0")
    nuetral_vader_score_range_count_31_40 = Column(String(255), default="0")
    nuetral_vader_score_range_count_41_50 = Column(String(255), default="0")
    nuetral_vader_score_range_count_51_60 = Column(String(255), default="0")
    nuetral_vader_score_range_count_61_70 = Column(String(255), default="0")
    nuetral_vader_score_range_count_71_80 = Column(String(255), default="0")
    nuetral_vader_score_range_count_81_90 = Column(String(255), default="0")
    nuetral_vader_score_range_count_91_100 = Column(String(255), default="0")
    compound_vader_score_range_count_1_10 = Column(String(255), default="0")
    compound_vader_score_range_count_11_20 = Column(String(255), default="0")
    compound_vader_score_range_count_21_30 = Column(String(255), default="0")
    compound_vader_score_range_count_31_40 = Column(String(255), default="0")
    compound_vader_score_range_count_41_50 = Column(String(255), default="0")
    compound_vader_score_range_count_51_60 = Column(String(255), default="0")
    compound_vader_score_range_count_61_70 = Column(String(255), default="0")
    compound_vader_score_range_count_71_80 = Column(String(255), default="0")
    compound_vader_score_range_count_81_90 = Column(String(255), default="0")
    compound_vader_score_range_count_91_100 = Column(String(255), default="0")

    total_tweets = Column(String(255), default='0')
    state = Column(ChoiceType([(abbr, abbr) for abbr in STATES.values()]))
    _candidate_pk = Column('candidate_pk', Integer,
                           ForeignKey(PresidentialCandidate.pk))

    candidate = relationship(
        'PresidentialCandidate',
        backref=backref('sentiments', lazy='dynamic')
    )

    def update_score(self, blob_score, pos_vader_score, neg_vader_score,
                     nuetral_vader_score, compound_vader_score):
        #self._sentiment = self._sentiment + score

        # Totals are string because maximum int size would be exceeded in
        # timeframe.
        self.total_tweets = str(int(self.total_tweets) + 1)
        self.blob_score_total = str(int(self.blob_score_total) + round(blob_score))
        self.pos_vader_score_total = str(int(self.pos_vader_score_total) + round(pos_vader_score))
        self.neg_vader_score_total = str(int(self.neg_vader_score_total) + round(neg_vader_score))
        self.nuetral_vader_score_total = str(int(self.nuetral_vader_score_total) + round(nuetral_vader_score))
        self.compound_vader_score_total = str(int(self.compound_vader_score_total) + round(compound_vader_score))
        vals = (
            (blob_score, "blob_score_range_count_"),
            (pos_vader_score, "pos_vader_score_range_count_"),
            (neg_vader_score, "neg_vader_score_range_count_"),
            (nuetral_vader_score, "nuetral_vader_score_range_count_"),
            (compound_vader_score, "compound_vader_score_range_count_"),
        )
        for score, prefix in vals:
            key = prefix + self._range(score)
            count = int(getattr(self, key))
            setattr(self, key, str(count + 1))

        session.add(self)
        session.commit()

    def _range(self, score):
        if score <= 0:
            return "0"
        elif score >= 91:
            return "91_100"
        for v in range(1, 100, 10):
            if score < v:
                return "{}_{}".format(v, v + 9)


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
        return (float(self._sentiment) / float(self.total_tweets)) * float(100)

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
