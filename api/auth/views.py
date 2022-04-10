from flask import (
    request,
    jsonify,
    Blueprint,
    current_app as app
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt)
from marshmallow import ValidationError

from api.api.schemas import UserSchema
from api.models import Customer, User
from api.extensions import (
    db,
    apispec,
    jwt,
    pwd_context, openid_connect)
from api.auth.helpers import (
    add_token_to_database,
    revoke_token,
    is_token_revoked)
from api.utils.models import save_to_db, ROLE_CUSTOMER

blueprint = Blueprint("auth", __name__, url_prefix="/auth")


@blueprint.route("/register", methods=["POST"])
def register_user():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    if not request.json.get("username"):
        return jsonify({"msg": "JSON missing username"}), 400

    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"msg": "Username already taken"}), 400

    request.json["active"] = True
    user_schema = UserSchema()
    user = user_schema.load(request.json)
    user.role = ROLE_CUSTOMER
    save_to_db(db, user)
    user_claims_ = {"id": user.id, "role": ROLE_CUSTOMER}
    access_token = create_access_token(
        identity=user.id,
        user_claims=user_claims_)
    refresh_token = create_refresh_token(
        identity=user.id,
        user_claims=user_claims_)
    # create a customer, only for simple auth purposes
    customer = Customer(
        name=username,
        email=user.email,
        user_id=user.id)
    save_to_db(db, customer)
    resp = {
        "user": user_schema.dump(user),
        "customer_id": customer.id,
        "access_token": access_token,
        "refresh_token": refresh_token}
    return jsonify(resp), 201


@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get("username")
    password = request.json.get("password")

    if not (username or password):
        return jsonify({"msg": "Missing username or password"}), 400

    try:
        token = openid_connect.token(username, password, totp="12345")
        user_info = openid_connect.userinfo(token['access_token'])
    except Exception as e:
        return jsonify({"message": f"Error occurred: {str(e)}"}), 401

    if not user_info:
        return jsonify({"msg": "Bad credentials"}), 400

    # access_token = create_access_token(identity=user.id)
    # refresh_token = create_refresh_token(identity=user.id)
    # add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    # add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    resp = {"access_token": token["access_token"], "refresh_token": token["refresh_token"]}
    return jsonify(resp), 200


@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    ret = {"access_token": access_token}
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    return jsonify(ret), 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return User.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=register_user, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
