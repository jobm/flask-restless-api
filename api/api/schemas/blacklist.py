from ...models import TokenBlacklist
from ...extensions import ma, db


class TokenBlacklistSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = TokenBlacklist
        sqla_session = db.session
        load_instance = True
