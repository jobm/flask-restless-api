import enum
import factory
import locale
import random
from faker import Faker

from api.models import Book


class Genres(enum.Enum):
    Fiction = "Fiction"
    Novel = "Novel"
    Regula = "Regular"


class BookFactory(factory.Factory):
    author = factory.LazyFunction(
        Faker(locale.getdefaultlocale()[0]).name)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=10)
    genre = factory.LazyFunction(
        lambda: random.choice([
            "Fiction",
            "Novel",
            "Regular"]))

    class Meta:
        model = Book
