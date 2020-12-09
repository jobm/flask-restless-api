from datetime import datetime

from api.extensions import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=False)
    title = db.Column(db.String(80), nullable=False)
    genre = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Book {}>'.format(self.id)
