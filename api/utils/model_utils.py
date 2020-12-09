# for simple auth, this should be a sqlalchemy object
ROLE_ADMIN = 'admin'
ROLE_CUSTOMER = 'customer'


def save_to_db(db, model, commit=True):
    db.session.add(model)
    if not commit:
        return
    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        raise err


def save_all_to_db(db, models, commit=True):
    db.session.add_all(models)
    if not commit:
        return
    try:
        db.session.commit()
    except Exception as err:
        db.session.rollback()
        raise err
