import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='super-secret',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from simta.db import init_dummy
    init_dummy()

    from simta.services.entities import User
    from simta.services.services import Revisi
    app.register_blueprint(User.bp)
    app.register_blueprint(Revisi.bp)

    jwt = JWTManager(app)

    api = Api(app)

    from simta.services.entities import Mahasiswa, Dosen, TA, TAList, Sidang, SidangList, Revisi, RevisiList, FormPomits
    api.add_resource(Mahasiswa, '/mahasiswa/<int:mhs_id>')
    api.add_resource(Dosen, '/dosen/<int:dosen_id>')
    api.add_resource(TA, '/ta/<int:ta_id>')
    api.add_resource(TAList, '/ta/')
    api.add_resource(Sidang, '/sidang/<int:sidang_id>', '/ta/<int:sidang_id>/sidang')
    api.add_resource(SidangList, '/sidang/')
    api.add_resource(Revisi, '/revisi/<int:revisi_id>')
    api.add_resource(RevisiList, '/sidang/<int:sidang_id>/revisi', '/ta/<int:sidang_id>/sidang/revisi', '/ta/<int:sidang_id>/revisi', '/revisi/sidang/<int:sidang_id>')
    api.add_resource(FormPomits, '/pomits/form/<int:sidang_id>', '/sidang/<int:sidang_id>/pomits/form', '/ta/<int:sidang_id>/sidang/pomits/form')

    CORS(app)

    return app
