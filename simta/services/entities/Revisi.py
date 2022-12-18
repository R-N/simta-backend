from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models
from simta.classes import Error

class Revisi(Resource):
    @jwt_required()
    def get(self, revisi_id):
        try:
            return models.Revisi.get(revisi_id)
        except Error as ex:
            return {"message": ex.message}, ex.code

class RevisiList(Resource):
    @jwt_required()
    def get(self, sidang_id):
        parser = reqparse.RequestParser()
        parser.add_argument("status", type=int, help="Status revisi")
        args = parser.parse_args()

        user_id = get_jwt_identity()

        try:
            return models.Revisi.fetch(sidang_id, user_id, **args)
        except Error as ex:
            return {"message": ex.message}, ex.code
