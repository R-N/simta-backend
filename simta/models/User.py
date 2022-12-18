from sqlalchemy import select
from flask_jwt_extended import create_access_token
from simta.classes import Error
from simta import db, util


allowed_fields = {"id", "name", "lab_id"}

def postprocess(user):
    user = util.filter_obj_dict(user, allowed_fields)
    return user

def login(username, password):
    with db.Session() as session:
        stmt = select(db.User).filter_by(username=username)
        user = session.scalars(stmt).first()

    if not user or not user.check_password(password):
        raise Error("User not found or wrong password", 401)

    return create_access_token(identity=user.id)

def get(user_id):
    with db.Session() as session:
        user = session.get(db.User, user_id)

    if not user:
        raise Error("User not found", 404)

    user = postprocess(user)

    return user
