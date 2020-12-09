from ...models import Cart
from ...extensions import ma, db


class CartSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Cart
        sqla_session = db.session
        load_instance = True
