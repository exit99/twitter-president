from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils.types.choice import ChoiceType

from constants import STATES
from extensions import Base, session
from mixins import ModelMixin


class PresidentialCandidate(ModelMixin, Base):
    __tablename__ = "presidential_candidate"
    pk = Column(Integer, primary_key=True)
    name = Column(String(120))

    def update_sentiment_score(self, state, score):
        ts = TweetSentiment.get_or_create(candidate=self, state=state)
        ts.update_score(score)

    def __repr__(self):
        return "<PresidentialCandidate '{}'>".format(self.name)


class TweetSentiment(ModelMixin, Base):
    __tablename__ = "candidate_tweet_sentiment"
    pk = Column(Integer, primary_key=True)
    sentiment = Column(Float, default=0.0)
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
        self.sentiment = (self.sentiment + score) / self.total_tweets
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<TweetSentiment '{}': '{}'>".format(self.candidate.name,
                                                    self.state)
