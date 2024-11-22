from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models
from simta.classes import Error

class Sidang(Resource):
    @jwt_required()
    def get(self, sidang_id):
        user_id = int(get_jwt_identity())
        try:
            return models.Sidang.get(sidang_id, user_id=user_id)
        except Error as ex:
            return {"show": True, "message": ex.message}, ex.code

class SidangList(Resource):
    @jwt_required()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument("mhs_id", type=int, help="Id mahasiswa sidang", location='args')
        parser.add_argument("pembimbing_id", type=int, help="Id pembimbing TA", location='args')
        parser.add_argument("penguji_id", type=int, help="Id penguji TA, termasuk pembimbing", location='args')
        parser.add_argument("type", type=int, help="Jenis TA (1=Request, 2=Proposal, 3=TA)", location='args')
        parser.add_argument("ta_type", type=int, help="Jenis TA (1=Request, 2=Proposal, 3=TA)", location='args')
        parser.add_argument("ta_status", type=int, help="Status TA", location='args')
        parser.add_argument("status", type=int, help="Status sidang", location='args')
        args = parser.parse_args()

        user_id = int(get_jwt_identity())
        args["user_id"] = user_id
        args["pembimbing_id"] = user_id
        args["penguji_id"] = user_id

        try:
            return models.Sidang.fetch(**args)
        except Error as ex:
            return {"show": True, "message": ex.message}, ex.code
