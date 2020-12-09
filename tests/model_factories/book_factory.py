import locale
import factory
from faker import Faker

from api.models import Book


class BookFactory(factory.Factory):
    author = factory.LazyFunction(
        Faker(locale.getdefaultlocale()[0]).name)
    title = factory.Faker('sentence', nb_words=4)
    description = factory.Faker('sentence', nb_words=10)

    class Meta:
        model = Book
