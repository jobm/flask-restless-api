import pytest
from flask import url_for

from api.models import Book


@pytest.fixture
def _book():
    return {
        "author": "Volkov Wolfgang",
        "description": "what a lovely piece of work",
        "title": "Ex Machina"}


def test_create_book(client, all_headers, _book):
    create_book_url = url_for("api.create_book")
    resp = client.post(
        create_book_url,
        json=_book,
        headers=all_headers["customer_headers"])
    assert resp.status_code == 401

    create_book_url = url_for("api.create_book")
    resp = client.post(
        create_book_url,
        json=_book,
        headers=all_headers["admin_headers"])
    assert resp.status_code == 201
    saved_book_id = resp.json["book"]["id"]
    assert Book.query.get(saved_book_id)


def test_update_book(client, all_headers, _book):
    create_book_url = url_for("api.create_book")
    resp = client.post(
        create_book_url,
        json=_book,
        headers=all_headers["admin_headers"])
    created_book_id = resp.json["book"]["id"]

    update_book_url = url_for("api.book_by_id", book_id=created_book_id)

    book_data = dict(_book)
    new_author = "jon snow"
    book_data["author"] = new_author

    resp = client.put(
        update_book_url,
        json=book_data,
        headers=all_headers["admin_headers"])
    updated_book_id = resp.json["book"]["id"]
    assert updated_book_id == created_book_id
    assert Book.query.get(updated_book_id).author == new_author


def test_delete_book(client, all_headers, _book):
    create_book_url = url_for("api.create_book")
    resp = client.post(
        create_book_url,
        json=_book,
        headers=all_headers["admin_headers"])

    created_book_id = resp.json["book"]["id"]

    delete_book_url = url_for("api.book_by_id", book_id=created_book_id)
    resp = client.delete(
        delete_book_url,
        headers=all_headers["admin_headers"])
    assert resp.status_code == 200


def test_get_all_books(client, db, all_headers, book_factory):
    books_url = url_for("api.all_books")
    resp = client.get(
        books_url,
        headers=all_headers["no_auth_headers"])
    assert resp.status_code == 200
    assert resp.json["total"] == 0

    default_num_books = 10
    books = book_factory.create_batch(default_num_books)

    db.session.add_all(books)
    db.session.commit()

    resp = client.get(
        books_url,
        headers=all_headers["no_auth_headers"])
    assert resp.status_code == 200
    assert resp.json["total"] == default_num_books
