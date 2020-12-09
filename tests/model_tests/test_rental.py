import pytest
from datetime import datetime

from api.utils.models import save_to_db

INVOICE_DUE_AT = datetime.utcnow()
INVOICE_AMOUNT = 10


@pytest.fixture
def _rental(db, book, customer, rental, user):
    save_to_db(db, book)
    save_to_db(db, user)

    customer.user_id = user.id
    save_to_db(db, customer)

    rental.customer_id = customer.id
    rental.book_id = book.id
    save_to_db(db, rental)

    return rental


def test_saves_invoice(_rental, customer, book):
    assert _rental.id
    assert _rental.created_at
    assert not _rental.due_at
    assert _rental.book_id == book.id
    assert _rental.customer_id == customer.id
