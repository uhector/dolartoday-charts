# -*- coding: utf-8 -*-

from app import db

from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):

    __tablename__ = 'USERS'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    hashed_pw = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, server_default='0', nullable=False)

    # server_default="50"

    def set_password(self, password):
        self.hashed_pw = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_pw, password)

    def __repr__(self):
        return '<User {}>'.format(self.id)


class PriceHistory(db.Model):

    __tablename__ = 'PRICE_HISTORY'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, index=True, unique=True, nullable=False)
    price = db.Column(db.Float, index=True, nullable=False)

    def __repr__(self):
        return '<PriceHistory {}>'.format(self.id)