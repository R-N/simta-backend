from flask_restful import Resource
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models
from simta.classes import Error

class Dosen(Resource):
    @jwt_required()
    def get(self, dosen_id):
        try:
            return models.Dosen.get(dosen_id)
        except Error as ex:
            return {"message": ex.message}, ex.code
