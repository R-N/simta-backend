from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta.classes import Error
from simta import models
from flask_restful import reqparse
from werkzeug.datastructures import FileStorage

bp = Blueprint('revisi', __name__, url_prefix='/revisi')

@bp.route('/<int:revisi_id>/terima', methods=('POST',))
@jwt_required()
def terima(revisi_id):
    user_id = get_jwt_identity()
    try:
        ret = models.Revisi.terima(revisi_id, user_id)
        ret["result"] = "success"
        return ret
    except Error as ex:
        return {"message": ex.message}, ex.code

@bp.route('/<int:revisi_id>/tolak', methods=('POST',))
@jwt_required()
def tolak(revisi_id):
    user_id = get_jwt_identity()
    data = request.json
    detail, file_name = data.get("detail", None), data.get("file_name", None)
    if not (detail):
        return {"result": "Must provide detail"}, 400

    try:
        models.Revisi.tolak(revisi_id, user_id, detail, file_name)
        return {"result": "success"}
    except Error as ex:
        return {"message": ex.message}, ex.code


@bp.route('/<int:revisi_id>/tolak/upload', methods=('PUT',))
@jwt_required()
def upload_feedback_penolakan(revisi_id):
    user_id = get_jwt_identity()
    parse = reqparse.RequestParser()
    parse.add_argument('file', type=FileStorage, location='files')
    args = parse.parse_args()
    file = args['file'] if "file" in args else None

    try:
        if file:
            file.save(f"assets/files/penolakan_revisi/{revisi_id}.pdf")
        return {"result": "success"}
    except Error as ex:
        return {"message": ex.message}, ex.code



