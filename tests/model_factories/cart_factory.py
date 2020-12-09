import factory

from api.models import Cart


class CartFactory(factory.Factory):

    class Meta:
        model = Cart
