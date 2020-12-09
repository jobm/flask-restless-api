from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from ..extensions import apispec
from .resources import (
    BookResource,
    BooksResource,
    CartItemsResource,
    CartOrderPrice,
    UserResource,
    UsersResource)
from .schemas import (
    BookSchema,
    CartSchema,
    CartItemSchema,
    CustomerSchema,
    UserSchema)


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# Book endpoints
api.add_resource(BookResource, "/books", endpoint="create_book")
api.add_resource(BookResource, "/books/<int:book_id>", endpoint="book_by_id")
api.add_resource(BooksResource, "/all-books", endpoint="all_books")


# Add items to Cart
api.add_resource(CartItemsResource, "/cart-items", endpoint="cart_items")

# Check Cost of Cart
api.add_resource(CartOrderPrice, "/cart/<int:cart_id>/order-price", endpoint="order_price")


# User endpoints
api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UsersResource, "/users", endpoint="users")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("BookSchema", schema=BookSchema)
    apispec.spec.components.schema("CustomerSchema", schema=CustomerSchema)
    apispec.spec.components.schema("CartSchema", schema=CartSchema)
    apispec.spec.components.schema("CartItemSchema", schema=CartItemSchema)
    apispec.spec.components.schema("UserSchema", schema=UserSchema)

    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UsersResource, app=current_app)

    apispec.spec.path(view=BookResource, app=current_app)
    apispec.spec.path(view=BooksResource, app=current_app)

    apispec.spec.path(view=CartItemsResource, app=current_app)
    apispec.spec.path(view=CartOrderPrice, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
