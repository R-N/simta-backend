from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models


allowed_fields = {"id", "nrp", "level"}
enums = ["level"]

def postprocess(mhs):
    user = mhs.user
    mhs = util.filter_obj_dict(mhs, allowed_fields)
    util.resolve_enums(mhs, enums)
    mhs = {
        **mhs,
        **models.User.postprocess(user)
    }
    return mhs

def get(mhs_id):
    with db.Session() as session:
        mhs = session.get(db.Mahasiswa, mhs_id)

        if not mhs:
            raise Error("Mahasiswa not found", 404)

        mhs = postprocess(mhs)
    return mhs
