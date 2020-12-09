import pytest

from api.models import CartItem
from api.utils.model_utils import save_to_db
from ..model_factories.cart_item_factory import CartItemFactory


@pytest.fixture
def _cart_item(db, book, cart, customer, user):
    save_to_db(db, user)

    customer.user_id = user.id
    save_to_db(db, customer)

    cart.customer_id = customer.id
    save_to_db(db, cart)

    save_to_db(db, book)

    cart_item = CartItemFactory(
        book_id=book.id,
        cart_id=cart.id)
    save_to_db(db, cart_item)

    cart.cart_items.append(cart_item)
    save_to_db(db, cart)
    save_to_db(db, cart_item)

    return cart_item


def test_save_book(_cart_item, cart, book):
    assert _cart_item.book_id == book.id
    assert _cart_item.cart_id == cart.id
    assert CartItem.query.get(_cart_item.id)
