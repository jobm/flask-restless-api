import pytz
from datetime import datetime

from api.extensions import db


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    book = db.relationship(
        'Book',
        backref=db.backref('cart_items', uselist=False))
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

    def __repr__(self):
        return '<CartItem {}>'.format(self.id)
