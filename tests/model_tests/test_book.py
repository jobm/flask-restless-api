import pytest

from api.models import Book
from ..model_factories.book_factory import BookFactory


@pytest.fixture
def book(db):
    book = BookFactory(author='Bilbo Baggins')
    db.session.add(book)
    db.session.commit()
    return book


def test_save_book(book):
    assert book.id
    assert book.title
    assert book.description
    assert book.created_at
    assert book.author == 'Bilbo Baggins'
    assert Book.query.get(book.id)
