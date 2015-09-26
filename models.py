from sqlalchemy_utils.types.choice import ChoiceType
from constants import STATES

from extensions import db
from mixins import ModelMixin


class PresidentialCandidate(ModelMixin, db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))

    def update_sentiment_score(self, state, score):
        ts = TweetSentiment.query.get_or_create(candidate=self, state=state)
        ts.update_score(score)

    def __repr__(self):
        return "<PresidentialCandidate '{}'>".format(self.name)


class TweetSentiment(ModelMixin, db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    sentiment = db.Column(db.Float, default=0.0)
    total_tweets = db.Column(db.Integer, default=0)
    state = db.Column(ChoiceType([(abbr, abbr) for abbr in STATES.values()]))
    _candidate_pk = db.Column('candidate_pk', db.Integer,
                              db.ForeignKey(PresidentialCandidate.pk))

    candidate = db.relationship(
        'PresidentialCandidate',
        backref=db.backref('sentiments', lazy='dynamic')
    )

    def update_score(self, score):
        self.total_tweets += 1
        self.sentiment = (self.sentiment + score) / self.total_tweets
        self.query.session.add(self)
        self.query.session.commit()

    def __repr__(self):
        return "<TweetSentiment '{}': '{}'>".format(self.candidate.name,
                                                    self.state)
