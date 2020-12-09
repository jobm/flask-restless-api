from flask import request
from flask_restful import Resource

from ...auth.helpers import admin_required
from ...extensions import db
from ...commons.pagination import paginate
from ...models.book import Book
from ..schemas.book import BookSchema
from ...utils.models import save_to_db


class BookResource(Resource):

    @staticmethod
    def get(book_id):
        book_schema = BookSchema()
        book = Book.query.get_or_404(book_id)
        return {"book": book_schema.dump(book)}, 200

    @staticmethod
    @admin_required
    def put(book_id):
        book_schema = BookSchema(partial=True)
        book = Book.query.get_or_404(book_id)
        book = book_schema.load(request.json, instance=book)
        db.session.commit()
        return {"msg": "book updated", "book": book_schema.dump(book)}, 201

    @staticmethod
    @admin_required
    def post():
        book_schema = BookSchema()
        book = book_schema.load(request.json)
        save_to_db(db, book)
        return {"msg": "book created", "book": book_schema.dump(book)}, 201

    @staticmethod
    @admin_required
    def delete(book_id):
        book = Book.query.get_or_404(book_id)
        db.session.delete(book)
        db.session.commit()
        return {"msg": "book deleted"}, 200


class BooksResource(Resource):

    @staticmethod
    def get():
        schema = BookSchema(many=True)
        query = Book.query
        return paginate(query, schema)
