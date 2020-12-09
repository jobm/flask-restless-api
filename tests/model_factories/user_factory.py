import locale
import factory
from faker import Faker
from uuid import uuid4

from api.models import User


class UserFactory(factory.Factory):

    email = factory.LazyFunction(
        lambda: Faker(locale.getdefaultlocale()[0]).email())
    password = factory.LazyFunction(lambda: str(uuid4()))
    username = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = User
