import json
import pytest
from dotenv import load_dotenv

from api.models import User
from api.app import create_app
from api.extensions import db as _db
from api.utils.model_utils import (
    ROLE_ADMIN,
    ROLE_CUSTOMER,
    save_to_db)
from pytest_factoryboy import register
from tests.model_factories.book_factory import BookFactory
from tests.model_factories.customer_factory import CustomerFactory
from tests.model_factories.cart_factory import CartFactory
from tests.model_factories.cart_item_factory import CartItemFactory
from tests.model_factories.rental_factory import RentalFactory
from tests.model_factories.user_factory import UserFactory


register(BookFactory)
register(CartFactory)
register(CartItemFactory)
register(CustomerFactory)
register(RentalFactory)
register(UserFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()


@pytest.fixture
def admin_user(db):
    user = User(
        username="admin",
        email="admin@lori.com",
        password="admin",
        role=ROLE_ADMIN,
        active=True)
    save_to_db(db, user)
    return user


@pytest.fixture
def customer_user(db):
    user_ = User(
        username="jon_doe",
        email="customer@example.com",
        password="123456",
        role=ROLE_CUSTOMER,
        active=True)
    save_to_db(db, user_)
    return user_


@pytest.fixture
def no_auth_headers():
    return {
        "content-type": "application/json",
        "authorization": ""
    }


@pytest.fixture
def customer_headers(db, customer_user, client, customer):
    data = {
        "username": customer_user.username,
        "password": '123456'
    }
    resp = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"}
    )
    customer.user_id = customer_user.id
    save_to_db(db, customer)
    tokens = json.loads(resp.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": f"Bearer {tokens['access_token']}"
    }


@pytest.fixture
def admin_headers(admin_user, client):
    data = {
        "username": admin_user.username,
        "password": 'admin'
    }
    resp = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"}
    )
    tokens = json.loads(resp.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": f"Bearer {tokens['access_token']}"
    }


@pytest.fixture
def admin_refresh_headers(admin_user, client):
    data = {
        "username": admin_user.username,
        "password": 'admin'
    }
    rep = client.post(
        "/auth/login",
        data=json.dumps(data),
        headers={"content-type": "application/json"}
    )

    tokens = json.loads(rep.get_data(as_text=True))
    return {
        "content-type": "application/json",
        "authorization": f"Bearer {tokens['refresh_token']}"
    }


@pytest.fixture
def all_headers(admin_headers, customer_headers, no_auth_headers):
    return {
        "admin_headers": admin_headers,
        "customer_headers": customer_headers,
        "no_auth_headers": no_auth_headers
    }
