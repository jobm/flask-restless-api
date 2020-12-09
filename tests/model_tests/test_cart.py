import pytest
from datetime import datetime

from api.utils.models import save_to_db

INVOICE_DUE_AT = datetime.utcnow()
INVOICE_AMOUNT = 10


@pytest.fixture
def _cart(db, cart, customer, user):
    save_to_db(db, user)

    customer.user_id = user.id
    save_to_db(db, customer)

    cart.customer_id = customer.id
    save_to_db(db, cart)

    return cart


def test_saves_invoice(_cart, customer):
    assert _cart.id
    assert _cart.created_at
    assert _cart.cart_items
    assert _cart.customer_id == customer.id
