from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta.classes import Error
from simta import models
from flask_restful import reqparse

bp = Blueprint('revisi', __name__, url_prefix='/revisi')

@bp.route('/<int:revisi_id>/terima', methods=('POST',))
@jwt_required()
def terima(revisi_id):
    user_id = int(get_jwt_identity())
    try:
        ret = models.Revisi.terima(revisi_id, user_id)
        ret["result"] = "success"
        return ret
    except Error as ex:
        return {"show": True, "message": ex.message}, ex.code

@bp.route('/<int:revisi_id>/tolak', methods=('POST',))
@jwt_required()
def tolak(revisi_id):
    user_id = int(get_jwt_identity())
    data = request.json
    detail, file_name = data.get("detail", None), data.get("file_name", None)
    if not (detail):
        return {"show": True, "message": "Must provide detail"}, 400

    try:
        models.Revisi.tolak(revisi_id, user_id, detail, file_name)
        return {"result": "success"}
    except Error as ex:
        return {"show": True, "message": ex.message}, ex.code
