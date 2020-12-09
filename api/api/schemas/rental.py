from ...models import Rental
from ...extensions import ma, db


class RentalSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Rental
        sqla_session = db.session
        load_instance = True
