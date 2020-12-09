import factory

from api.models import CartItem


class CartItemFactory(factory.Factory):

    class Meta:
        model = CartItem
