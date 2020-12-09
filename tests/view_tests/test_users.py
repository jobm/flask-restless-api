from flask import url_for
from scalpl import Cut

from api.utils.models import save_to_db
from api.extensions import pwd_context
from api.models import User


def test_get_user(client, db, user, admin_headers):
    # test 404
    user_url = url_for('api.user_by_id', user_id="100000")
    resp = client.get(user_url, headers=admin_headers)
    assert resp.status_code == 404

    save_to_db(db, user)
    user_url = url_for('api.user_by_id', user_id=user.id)
    resp = client.get(user_url, headers=admin_headers)
    assert resp.status_code == 200

    data = resp.get_json()["user"]
    assert data["username"] == user.username
    assert data["email"] == user.email
    assert data["active"] == user.active


def test_put_user(client, db, user, admin_headers):
    user_url = url_for('api.user_by_id', user_id="100000")
    rep = client.put(user_url, headers=admin_headers)
    assert rep.status_code == 404

    save_to_db(db, user)

    data = {"username": "updated", "password": "new_password"}

    user_url = url_for('api.user_by_id', user_id=user.id)

    resp = client.put(user_url, json=data, headers=admin_headers)
    assert resp.status_code == 200

    data = resp.get_json()["user"]
    assert data["username"] == "updated"
    assert data["email"] == user.email
    assert data["active"] == user.active

    db.session.refresh(user)
    assert pwd_context.verify("new_password", user.password)


def test_delete_user(client, db, user, admin_headers):
    user_url = url_for('api.user_by_id', user_id="100000")
    rep = client.delete(user_url, headers=admin_headers)
    assert rep.status_code == 404

    save_to_db(db, user)

    user_url = url_for('api.user_by_id', user_id=user.id)
    rep = client.delete(user_url,  headers=admin_headers)
    assert rep.status_code == 200
    assert db.session.query(User).filter_by(id=user.id).first() is None


def test_create_user(client, db, admin_headers):
    # test bad data
    register_user_url = url_for('auth.register_user')
    data = {"username": "created"}
    rep = client.post(register_user_url, json=data, headers=admin_headers)
    assert rep.status_code == 400

    data["password"] = "admin"
    data["email"] = "create@mail.com"

    resp = client.post(register_user_url, json=data, headers=admin_headers)
    assert resp.status_code == 201

    data = Cut(resp.get_json())
    id_ = data["user.id"]
    user = db.session.query(User).filter_by(id=id_).first()
    assert user.username == "created"
    assert user.email == "create@mail.com"


def test_get_all_user(client, db, user_factory, admin_headers):
    users_url = url_for('api.users')
    users = user_factory.create_batch(30)

    db.session.add_all(users)
    db.session.commit()

    rep = client.get(users_url, headers=admin_headers)
    assert rep.status_code == 200

    results = rep.get_json()
    for user in users:
        assert any(u["id"] == user.id for u in results["results"])
