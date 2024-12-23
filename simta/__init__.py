import os
import shutil
import datetime
import logging
import sys

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

WORKDIR = os.getenv("WORKDIR")
if WORKDIR:
    if os.path.isdir(f"{WORKDIR}/assets"):
        shutil.rmtree(f"{WORKDIR}/assets")
    shutil.copytree("simta/assets/", f"{WORKDIR}/assets", dirs_exist_ok=True)

LOG_DIR = os.getenv("LOG_DIR")

def create_app(test_config=None, force_init_dummy=True):
    # create and configure the app
    if LOG_DIR:
        path = Path(LOG_DIR)
        path.mkdir(parents=True, exist_ok=True)
        ct = datetime.datetime.now()
        logging.basicConfig(
            filename=os.path.join(
                LOG_DIR,
                f"{ct}.log".replace(":","-")
            ), level=logging.DEBUG
        )
        """
        logger = logging.getLogger()
        sys.stderr.write = logger.error
        sys.stdout.write = logger.info
        """

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
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from simta.db import init_dummy
    init_dummy(force_init_dummy)

    from simta.services.entities import User
    from simta.services.services import Revisi
    app.register_blueprint(User.bp)
    app.register_blueprint(Revisi.bp)

    jwt = JWTManager(app)

    api = Api(app)

    from simta.services.entities import Mahasiswa, Dosen, TA, TAList, Sidang, SidangList, Revisi, RevisiList, FilePenolakanRevisi, FormPomits, FileRevisi
    api.add_resource(Mahasiswa, '/mahasiswa/<int:mhs_id>')
    api.add_resource(Dosen, '/dosen/<int:dosen_id>')
    api.add_resource(TA, '/ta/<int:ta_id>')
    api.add_resource(TAList, '/ta/')
    api.add_resource(Sidang, '/sidang/<int:sidang_id>', '/ta/<int:sidang_id>/sidang')
    api.add_resource(SidangList, '/sidang/')
    api.add_resource(Revisi, '/revisi/<int:revisi_id>')
    api.add_resource(RevisiList, '/sidang/<int:sidang_id>/revisi', '/ta/<int:sidang_id>/sidang/revisi', '/ta/<int:sidang_id>/revisi', '/revisi/sidang/<int:sidang_id>')
    api.add_resource(FileRevisi, '/revisi/<int:revisi_id>/file')
    api.add_resource(FilePenolakanRevisi, '/revisi/<int:revisi_id>/penolakan/file')
    api.add_resource(FormPomits, '/pomits/form/<int:sidang_id>', '/sidang/<int:sidang_id>/pomits/form', '/ta/<int:sidang_id>/sidang/pomits/form')

    CORS(app)

    return app
