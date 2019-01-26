from datetime import datetime
from uuid import uuid4

from . import db


class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    votings = db.relationship('Voting', backref='user', lazy=True)
    votes = db.relationship('Vote', backref='user', lazy=True)

    def __repr__(self):
        '<User {}>'.format(self.username)


class Voting(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    creator = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    nomination_end = db.Column(db.DateTime, default=None)
    voting_end = db.Column(db.DateTime)
    config = db.Column(db.Text)
    votes = db.relationship('Vote', backref='voting', lazy=True)

    def __repr__(self):
        '<Voting {}>'.format(self.title)


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voting_id = db.Column(db.String, db.ForeignKey('voting.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)


class Alternative(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voting_id = db.Column(db.String, db.ForeignKey('voting.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    link = db.Column(db.String(300))
    score = db.Column(db.Integer, default=0)
