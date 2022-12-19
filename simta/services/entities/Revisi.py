from flask_restful import Resource, reqparse
from flask import jsonify, send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models, db
from simta.classes import Error
from werkzeug.datastructures import FileStorage

class Revisi(Resource):
    @jwt_required()
    def get(self, revisi_id):
        user_id = get_jwt_identity()
        try:
            return models.Revisi.get(revisi_id, user_id)
        except Error as ex:
            return {"message": ex.message}, ex.code

class FilePenolakanRevisi(Resource):
    @jwt_required()
    def get(self, revisi_id):
        user_id = get_jwt_identity()
        try:
            return models.Revisi.download_file_penolakan(revisi_id, user_id)
        except Error as ex:
            return {"message": ex.message}, ex.code

    @jwt_required()
    def put(self, revisi_id):
        user_id = get_jwt_identity()
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=FileStorage, location='files')
        args = parse.parse_args()
        file = args['file'] if "file" in args else None
        if not file:
            return {"result": "Must provide file"}, 400
        try:
            models.Revisi.upload_file_penolakan(revisi_id, file, user_id)
            return {"result": "success"}
        except Error as ex:
            return {"message": ex.message}, ex.code


class RevisiList(Resource):
    @jwt_required()
    def get(self, sidang_id):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=int, help="Status revisi", location='args')
        args = parser.parse_args()
        try:
            return models.Revisi.fetch(sidang_id, user_id, **args)
        except Error as ex:
            return {"message": ex.message}, ex.code
