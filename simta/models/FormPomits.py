from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models


allowed_fields = {
    "id", "check_1", "check_2", "check_3"
}

DEFAULT_SIDANG = True
DEFAULT_PENGUJI = False
DEFAULT_PEMBIMBING = False
DEFAULT_REVISI_TERAKHIR = False
DEFAULT_TA = True
DEFAULT_MHS = True

def postprocess(form_pomits, sidang=DEFAULT_SIDANG, penguji=DEFAULT_PENGUJI, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, mhs=DEFAULT_MHS, **kwargs):
    if sidang:
        sidang = form_pomits.sidang

    form_pomits = util.filter_obj_dict(form_pomits, allowed_fields)

    if sidang:
        sidang = models.Sidang.postprocess(
            sidang,
            penguji=penguji,
            ta=ta,
            pembimbing=pembimbing,
            revisi_terakhir=revisi_terakhir,
            mhs=mhs,
            **kwargs
        )
        form_pomits["sidang"] = sidang

    return form_pomits


def get(sidang_id, penguji=DEFAULT_PENGUJI, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, mhs=DEFAULT_MHS, **kwargs):
    with db.Session() as session:
        stmt = select(db.FormPomits)
        stmt = stmt.filter_by(id=sidang_id)

        form_pomits = session.scalars(stmt).first()

        if not form_pomits:
            raise Error("Form POMITS not found", 404)

        form_pomits = postprocess(
            form_pomits,
            penguji=penguji,
            ta=ta,
            pembimbing=pembimbing,
            revisi_terakhir=revisi_terakhir,
            mhs=mhs,
            **kwargs
        )
    return form_pomits
