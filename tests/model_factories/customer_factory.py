import locale
import factory
from faker import Faker

from api.models import Customer


class CustomerFactory(factory.Factory):
    name = factory.LazyFunction(
        Faker(locale.getdefaultlocale()[0]).name)
    email = factory.LazyFunction(
        lambda: Faker(locale.getdefaultlocale()[0]).email())

    class Meta:
        model = Customer
