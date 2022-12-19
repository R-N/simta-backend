from flask_restful import Resource, reqparse
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from simta import models
from simta.classes import Error

class FormPomits(Resource):
    @jwt_required()
    def get(self, sidang_id):
        user_id = get_jwt_identity()
        try:
            return models.FormPomits.get(sidang_id, user_id)
        except Error as ex:
            return {"message": ex.message}, ex.code
