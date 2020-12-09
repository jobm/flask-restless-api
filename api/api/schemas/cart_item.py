from ...models import CartItem
from ...extensions import ma, db


class CartItemSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = CartItem
        sqla_session = db.session
        load_instance = True
