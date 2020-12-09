import pytest

from api.models import Customer
from api.utils.model_utils import save_to_db
from ..model_factories.customer_factory import CustomerFactory
from ..model_factories.user_factory import UserFactory


@pytest.fixture
def customer(db):
    user = UserFactory()
    save_to_db(db, user)

    customer = CustomerFactory(
        name='John Doe',
        user_id=user.id)
    save_to_db(db, customer)
    return customer


def test_save_book(customer):
    assert customer.id
    assert customer.email
    assert customer.created_at
    assert customer.user_id
    assert customer.name == 'John Doe'
    assert Customer.query.get(customer.id)
