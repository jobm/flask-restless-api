import pytz
from datetime import datetime

from api.extensions import db


class Cart(db.Model):
    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    cart_items = db.relationship(
        'CartItem',
        uselist=True,
        foreign_keys='CartItem.cart_id',
        backref='cart',
        lazy='dynamic',
        cascade='all, delete-orphan')
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

    def __repr__(self):
        return '<Cart {}>'.format(self.id)
