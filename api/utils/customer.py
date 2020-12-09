from api.models import Customer
from api.models import User
from api.extensions import db


def create_customer(user_id):
    user = User.query.get_or_404(user_id)
    customer = Customer(
        name=user.username,
        email=user.email,
        user=user)
    db.session.add(customer)
    db.session.commit()
    return customer
