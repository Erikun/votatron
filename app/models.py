from datetime import datetime
from uuid import uuid4

from . import db


class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    polls = db.relationship('Poll', backref='user')
    votes = db.relationship('Vote', backref='user', lazy=True)
    nominations = db.relationship('Alternative', backref='user', lazy=True)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Poll(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    creator = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    voting_start = db.Column(db.DateTime, default=None)
    voting_end = db.Column(db.DateTime)
    config = db.Column(db.Text)
    votes = db.relationship('Vote', backref='poll', lazy=True)
    alternatives = db.relationship('Alternative', backref='poll', lazy=True)

    def __repr__(self):
        return '<Poll {}>'.format(self.title)

    def is_nominating(self, t):
        "Whether the poll is in the nomination stage at the given time."
        return self.voting_start is None or t < self.voting_start

    def is_voting(self, t):
        "Whether the poll is in the voting stage at the given time."
        return self.voting_start and self.voting_start <= t and (
            self.voting_end is None or t < self.voting_end)

    def is_done(self, t):
        "Whether the poll is finished at the given time."
        return self.voting_end and self.voting_end <= t

    def has_voted(self, username):
        vote = (db.session.query(Vote)
                .filter(Vote.username == username)
                .filter(Vote.poll_id == self.id)
                .first())
        return vote
        

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.String, db.ForeignKey('poll.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)


class Alternative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.String, db.ForeignKey('poll.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    creator = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    link = db.Column(db.String(300))
    score = db.Column(db.Integer, default=0)
