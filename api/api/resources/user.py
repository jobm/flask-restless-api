from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ...api.schemas import UserSchema
from ...models import User
from ...extensions import db
from ...commons.pagination import paginate


class UserResource(Resource):

    method_decorators = [jwt_required]

    @staticmethod
    def get(user_id):
        user_schema = UserSchema()
        user = User.query.get_or_404(user_id)
        return {"user": user_schema.dump(user)}

    @staticmethod
    def put(user_id):
        schema = UserSchema(partial=True)
        user = User.query.get_or_404(user_id)
        user = schema.load(request.json, instance=user)
        db.session.add(user)
        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    @staticmethod
    def delete(user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}


class UsersResource(Resource):

    method_decorators = [jwt_required]

    @staticmethod
    def get():
        schema = UserSchema(many=True)
        query = User.query
        return paginate(query, schema)

