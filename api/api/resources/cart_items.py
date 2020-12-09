import pytz
from datetime import datetime

from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, inputs

from ...extensions import db
from ...api.schemas import CartSchema, CartItemSchema, RentalSchema
from ...models import Cart, Customer, CartItem, Rental
from ...utils.model_utils import save_to_db, save_all_to_db


class CartItemsResource(Resource):

    @staticmethod
    def create_rental(book_id, customer_id, due_at):
        rental = Rental(
            customer_id=customer_id,
            book_id=book_id,
            due_at=due_at)
        save_to_db(db, rental)
        return rental

    @staticmethod
    def create_cart_item(book_id, cart_id):
        cart_item = CartItem(
            book_id=book_id,
            cart_id=cart_id)
        return cart_item

    @staticmethod
    def get_or_create_customer_cart(customer_id):
        cart = Cart.query.filter_by(
            customer_id=customer_id).first()
        if not cart:
            cart = Cart(customer_id=customer_id)
            save_to_db(db, cart)
            return cart
        return cart

    @jwt_required
    def post(self):
        user_id = current_user.id
        customer = Customer.query.filter_by(
            user_id=user_id).first()
        cart = self.get_or_create_customer_cart(
            customer.id)

        try:
            items = request.json['items']
            if not items:
                raise IndexError
        except (KeyError, IndexError):
            return {"message": "Invalid json"}, 400

        _cart_items = []
        rentals = []
        for it in items:
            cart_item = self.create_cart_item(
                it['book_id'],
                cart.id)
            _cart_items.append(cart_item)
            rental = self.create_rental(
                it["book_id"],
                customer.id,
                inputs.datetime_from_rfc822(it['due_at']))
            rentals.append(rental)
        save_all_to_db(db, _cart_items)

        cart.cart_items.extend(_cart_items)
        save_to_db(db, cart)
        cart_schema = CartSchema()
        cart_item_schema = CartItemSchema(many=True)
        rental_schema = RentalSchema(many=True)
        resp_data = {
            "data": {
                "cart": cart_schema.dump(cart),
                "cart_items": cart_item_schema.dump(_cart_items),
                "rentals": rental_schema.dump(rentals)}}
        return resp_data, 201


class CartOrderPrice(Resource):

    method_decorators = [jwt_required]

    @staticmethod
    def num_of_days(due_at):
        today = datetime.now(pytz.utc)
        due_at = due_at.astimezone(pytz.utc)
        return (due_at - today).days or 1

    def get(self, cart_id):
        cart = Cart.query.get_or_404(cart_id)
        rentals = Rental.query.join(
            CartItem,
            CartItem.book_id == Rental.book_id
        ).filter_by(cart_id=cart.id).all()
        num_books = len(rentals)
        total_days = sum([
            self.num_of_days(rental.due_at)
            for rental in rentals])
        return {"cost_usd": total_days * num_books}, 200
