import pytz

from api.extensions import db
from datetime import datetime

PENDING = "PENDING"
RENTED = "RENTED"
CANCELLED = "CANCELLED"


class Rental(db.Model):
    __tablename__ = "rentals"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    due_at = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(80), default=PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(pytz.utc))

    def __repr__(self):
        return '<Rental {}>'.format(self.id)
