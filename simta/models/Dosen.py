from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models


allowed_fields = {"id", "nip", "ttd"}

def postprocess(dosen):
    user = dosen.user
    dosen = util.filter_obj_dict(dosen, allowed_fields)
    dosen = {
        **dosen,
        **models.User.postprocess(user)
    }
    return dosen

def get(dosen_id):
    with db.Session() as session:
        dosen = session.get(db.Dosen, dosen_id)

        if not dosen:
            raise Error("Dosen not found", 404)

        dosen = postprocess(dosen)
    return dosen
