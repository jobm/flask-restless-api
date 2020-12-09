import pytest

from api.models import User
from api.utils.models import ROLE_CUSTOMER, save_to_db
from ..model_factories.user_factory import UserFactory


@pytest.fixture
def customer_user(db):
    customer_user = UserFactory(
        username='ruby',
        role=ROLE_CUSTOMER)
    save_to_db(db, customer_user)
    return customer_user


def test_user(customer_user):
    assert customer_user.id
    assert customer_user.email
    assert customer_user.username == 'ruby'
    assert customer_user.password != 'mordor'
    assert not customer_user.active
    assert User.query.get(customer_user.id)
