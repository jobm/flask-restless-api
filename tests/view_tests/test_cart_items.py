import pytest
import pytz
from flask import url_for
from datetime import datetime, timedelta
from scalpl import Cut

from api.utils.model_utils import (
    save_to_db,
    save_all_to_db
)

NUM_BOOKS = 3
TWO_DAYS = 2
FOUR_DAYS = 4
FIVE_DAYS = 5


@pytest.fixture
def _items_data(db, book_factory):
    books = book_factory.create_batch(NUM_BOOKS)
    save_all_to_db(db, books)
    items = [
        {"book_id": books[0].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=TWO_DAYS)},
        {"book_id": books[1].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=FOUR_DAYS)},
        {"book_id": books[1].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=FIVE_DAYS)}]
    return items


class TestCartItemsResource:
    @staticmethod
    def test_create_cart_items(
            client,
            db,
            customer,
            all_headers,
            _items_data):
        cart_items_url = url_for("api.cart_items")
        resp = client.post(
            cart_items_url,
            json={'items': 'bar'},
            headers=all_headers['no_auth_headers'])
        assert resp.status_code == 401

        resp = client.post(
            cart_items_url,
            json={"items": None},
            headers=all_headers['customer_headers'])
        assert resp.status_code == 400

        save_to_db(db, customer)

        resp = client.post(
            cart_items_url,
            json={"items": _items_data},
            headers=all_headers['customer_headers'])

        assert resp.status_code == 201


class TestCartOrderPrice:

    @staticmethod
    def test_get_order_price(client, _items_data, all_headers):
        cart_items_url = url_for("api.cart_items")
        resp = client.post(
            cart_items_url,
            json={"items": _items_data},
            headers=all_headers['customer_headers'])

        resp_data = Cut(resp.json)
        cart_id = resp_data["data.cart.id"]

        order_price_url = url_for("api.order_price", cart_id=-10)
        resp = client.get(
            order_price_url,
            headers=all_headers['customer_headers'])
        assert resp.status_code == 404

        order_price_url = url_for("api.order_price", cart_id=cart_id)
        resp = client.get(
            order_price_url,
            headers=all_headers['no_auth_headers'])
        assert resp.status_code == 401

        resp = client.get(
            order_price_url,
            headers=all_headers["customer_headers"])
        assert resp.status_code == 200

        days = [TWO_DAYS, FOUR_DAYS, FIVE_DAYS]
        total_days = sum(days) - len(days)
        assert resp.json["cost_usd"] == total_days * NUM_BOOKS
