from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models
from simta.classes import Error

class Mahasiswa(Resource):
    @jwt_required()
    def get(self, mhs_id):
        try:
            return models.Mahasiswa.get(mhs_id)
        except Error as ex:
            return {"show": True, "message": ex.message}, ex.code
