import re
from functools import wraps
from flask import request
from typing import Dict
from extensions import admin, openidc
from api.config import KEYCLOAK_JWT_HEADER_NAME


TOKEN_ERROR_MSG = "Error Getting Token"

class AuthException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        dict_ = dict(self.payload or ())
        dict_["message"] = self.message
        return dict_


def get_user_token(username: str, password: str) -> Dict:
    try:
        token = openidc.token(username, password)
        return token["access_token"]
    except Exception as e:
        raise AuthException(
            TOKEN_ERROR_MSG, status_code=401, payload=("extra_info", str(e))
        )


def verify_access_token_active(access_token: str) -> bool:
    try:
        g = re.match(r"^Bearer\s+(.*)", access_token)
        if g:
            token = g.group(1)
        else:
            token = access_token
        token_info = openidc.introspect(token)
        if not (token_info and token_info.get("active")):
            return False
        return True
    except Exception as e:
        raise AuthException(
            "Error Verifying Token", status_code=401, payload=("extra_info", str(e))
        )


def refresh_token(oidc_obj: openidc, refresh_token_: str) -> str:
    try:
        return oidc_obj.refresh_token(refresh_token_)
    except Exception as e:
        raise AuthException(
            "Error Refreshing Token", status_code=401, payload=("extra_info", str(e))
        )


def get_userinfo(access_token: str) -> Dict:
    try:
        g = re.match(r"^Bearer\s+(.*)", access_token)
        if g:
            token = g.group(1)
        else:
            token = access_token

        user_info = openidc.userinfo(token)
        if not user_info:
            raise AuthException(
                "Missing User Info", status_code=404, payload=("extra_info", "")
            )
        return user_info
    except Exception as e:
        raise AuthException(
            TOKEN_ERROR_MSG, status_code=401, payload=("extra_info", str(e))
        )


def get_user(user_id: str) -> Dict:
    try:
        user = admin.get_user(user_id)
        return user
    except Exception as e:
        raise AuthException(
            TOKEN_ERROR_MSG, status_code=404, payload=("extra_info", str(e))
        )


def token_required(fn):
    """
    Role decorator that requires a valid token from Keycloak to
    """

    @wraps(fn)
    def decorator(*args, **kwargs):

        access_token = request.headers[KEYCLOAK_JWT_HEADER_NAME]

        if not verify_access_token_active(access_token):
            raise AuthException(
                "Invalid Token",
                status_code=401,
                payload={"extra_info": "Token is either Invalid/Expired"},
            )
        return fn(*args, **kwargs)

    return decorator
