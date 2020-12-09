import pytest
import pytz
from flask import url_for
from datetime import datetime, timedelta
from scalpl import Cut

from api.api.resources import CartOrderPrice
from api.utils.models import (
    save_to_db,
    save_all_to_db
)
from api.utils.cart_items import (
    MIN_FICTION_COST,
    MIN_NOVEL_COST,
    MIN_REGULAR_COST
)

NUM_BOOKS = 3
TWO_DAYS = 2
FOUR_DAYS = 4
FIVE_DAYS = 5


@pytest.fixture
def _items_data(db, book_factory):
    books = book_factory.create_batch(NUM_BOOKS)
    books[0].genre = "Fiction"
    books[1].genre = "Regular"
    books[2].genre = "Novel"
    save_all_to_db(db, books)
    items = [
        {"book_id": books[0].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=TWO_DAYS)},
        {"book_id": books[1].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=FOUR_DAYS)},
        {"book_id": books[2].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=FIVE_DAYS)}]
    return items


@pytest.fixture
def _items_data_min_days(db, book_factory):
    books = book_factory.create_batch(NUM_BOOKS)
    books[0].genre = "Fiction"
    books[1].genre = "Regular"
    books[2].genre = "Novel"
    save_all_to_db(db, books)
    items = [
        {"book_id": books[0].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=1)},
        {"book_id": books[1].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=1)},
        {"book_id": books[2].id,
         "due_at": datetime.now(pytz.utc) + timedelta(days=1)}]
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
            json={"items": "bar"},
            headers=all_headers["no_auth_headers"])
        assert resp.status_code == 401

        resp = client.post(
            cart_items_url,
            json={"items": None},
            headers=all_headers["customer_headers"])
        assert resp.status_code == 400

        save_to_db(db, customer)

        resp = client.post(
            cart_items_url,
            json={"items": _items_data},
            headers=all_headers["customer_headers"])
        assert resp.status_code == 201


class TestCartOrderPrice:

    @staticmethod
    def test_get_book_cost(db, book):
        fiction_book_price = 3
        book.genre = "Fiction"
        save_to_db(db, book)

        today = datetime.now(pytz.utc)
        due_at = datetime.now(pytz.utc) + timedelta(days=3)
        cost = CartOrderPrice.get_book_cost(
            book.id,
            today,
            due_at)
        assert cost == (due_at - today).days or 1 * \
               fiction_book_price

        due_at = datetime.now(pytz.utc) + timedelta(days=1)
        cost = CartOrderPrice.get_book_cost(
            book.id,
            today,
            due_at)
        assert cost == (due_at - today).days or 1 * \
               fiction_book_price

    @staticmethod
    def test_get_order_price(client, _items_data, all_headers):
        cart_items_url = url_for("api.cart_items")
        resp = client.post(
            cart_items_url,
            json={"items": _items_data},
            headers=all_headers["customer_headers"])

        resp_data = Cut(resp.json)
        cart_id = resp_data["data.cart.id"]

        order_price_url = url_for("api.order_price", cart_id=-10)
        resp = client.get(
            order_price_url,
            headers=all_headers["customer_headers"])
        assert resp.status_code == 404

        order_price_url = url_for("api.order_price", cart_id=cart_id)
        resp = client.get(
            order_price_url,
            headers=all_headers["no_auth_headers"])
        assert resp.status_code == 401

        resp = client.get(
            order_price_url,
            headers=all_headers["customer_headers"])
        assert resp.status_code == 200

        fiction_cost = TWO_DAYS * MIN_FICTION_COST
        novel_cost = FIVE_DAYS * 1.5
        regular_cost = FOUR_DAYS * 1.5
        sum_book_cost = fiction_cost + novel_cost + regular_cost
        assert resp.json["cost_usd"] == sum_book_cost

    @staticmethod
    def test_get_order_price_min_days(
            client,
            all_headers,
            _items_data_min_days):
        cart_items_url = url_for("api.cart_items")
        resp = client.post(
            cart_items_url,
            json={"items": _items_data_min_days},
            headers=all_headers["customer_headers"])
        assert resp.status_code == 201

        resp_data = Cut(resp.json)
        cart_id = resp_data["data.cart.id"]

        order_price_url = url_for("api.order_price", cart_id=cart_id)
        resp = client.get(
            order_price_url,
            headers=all_headers["customer_headers"])
        assert resp.status_code == 200

        assert resp.json["cost_usd"] == sum([
            MIN_FICTION_COST,
            MIN_NOVEL_COST,
            MIN_REGULAR_COST
        ])
