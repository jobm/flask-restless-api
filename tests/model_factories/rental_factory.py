import factory
import random

from api.models import Rental
from api.models.rental import (
    CANCELLED,
    PENDING,
    RENTED
)


class RentalFactory(factory.Factory):

    status = factory.LazyFunction(
        lambda: random.choice([CANCELLED, PENDING, RENTED]))

    class Meta:
        model = Rental
