from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required, verify_jwt_in_request
from simta.classes import Error
from simta import models
import traceback

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/login', methods=('POST',))
def login():
    data = request.json
    username, password = data.get("username", None), data.get("password", None)

    if not (username and password):
        return {"show": True, "message": "Must provide username and password"}, 400

    try:
        api_key = models.User.login(username, password)
        print("api_key")
        print(api_key)
        return {"api_key": api_key}
    except Error as ex:
        return {"show": True, "message": ex.message}, ex.code

@bp.route('/current', methods=('GET',))
@jwt_required()
def get_current():
    user_id = int(get_jwt_identity())
    try:
        return models.User.get(user_id)
    except Error as ex:
        return {"show": True, "message": ex.message}, ex.code


