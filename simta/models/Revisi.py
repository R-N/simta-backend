from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models

allowed_fields = {
    "id", "sidang_id", "penguji_id", "nomor", "status", "created_at", "updated_at", "file_name", "detail"
}
allowed_fields_penolakan = {
    "file_name", "detail"
}
allowed_filters = {"status"}
enums = ["status"]
strs = ["created_at", "updated_at"]

DEFAULT_SIDANG = True
DEFAULT_PENGUJI = False
DEFAULT_PENOLAKAN = True
DEFAULT_PEMBIMBING = False
DEFAULT_TA = True
DEFAULT_MHS = True
DEFAULT_REVISI_TERAKHIR = False


def apply_filters(stmt, **kwargs):
    return util.apply_filters(stmt, allowed_filters, kwargs)


def postprocess(revisi, sidang=DEFAULT_SIDANG, penguji=DEFAULT_PENGUJI, penolakan=DEFAULT_PENOLAKAN, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, **kwargs):
    if penolakan:
        penolakan = revisi.penolakan
        #penolakan = penolakan[0] if penolakan else None
    if sidang:
        sidang = revisi.penguji.sidang

    revisi = util.filter_obj_dict(revisi, allowed_fields)
    util.resolve_enums(revisi, enums)
    util.resolve_strs(revisi, strs)

    if sidang:
        sidang = models.Sidang.postprocess(
            sidang, 
            pembimbing=pembimbing, 
            penguji=penguji, 
            ta=ta,
            mhs=mhs, 
            revisi_terakhir=revisi_terakhir,
            **kwargs
        )
        revisi["sidang"] = sidang
    if penolakan:
        penolakan = util.filter_obj_dict(penolakan, allowed_fields_penolakan)
        revisi["penolakan"] = penolakan

    return revisi


def get(revisi_id, sidang=DEFAULT_SIDANG, penguji=DEFAULT_PENGUJI, penolakan=DEFAULT_PENOLAKAN, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, **kwargs):
    with db.Session() as session:
        stmt = select(db.Revisi)
        stmt = stmt.filter_by(id=revisi_id)

        revisi = session.scalars(stmt).first()

        if not revisi:
            raise Error("Revisi not found", 404)

        revisi = postprocess(
            revisi, 
            sidang=sidang,
            penguji=penguji,
            penolakan=penolakan,
            pembimbing=pembimbing,
            ta=ta,
            mhs=mhs,
            revisi_terakhir=revisi_terakhir,
            **kwargs
        )
    return revisi


def fetch_0(sidang_id, penguji_id, sidang=False, penguji=DEFAULT_PENGUJI, penolakan=DEFAULT_PENOLAKAN, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, status=None, **kwargs):
    with db.Session() as session:
        sidang = models.Sidang._get(session, sidang_id)
        _penguji = [p for p in sidang.penguji if p.id==penguji_id]
        if not _penguji:
            raise Error("Anda bukan penguji TA ini", 401)
        revisi = _penguji[0].revisi
        if status:
            revisi = [r for r in revisi if r.status==status]

        revisi = [postprocess(
            x,
            sidang=sidang,
            penguji=penguji,
            penolakan=penolakan,
            ta=ta,
            pembimbing=pembimbing,
            mhs=mhs,
            revisi_terakhir=revisi_terakhir,
            **kwargs
        ) for x in revisi]
    return revisi

def fetch(sidang_id, penguji_id, penguji=DEFAULT_PENGUJI, penolakan=DEFAULT_PENOLAKAN, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, status=None, **kwargs):
    sidang = models.Sidang.get(
        sidang_id=sidang_id, 
        user_id=penguji_id,
        ta=ta,
        pembimbing=pembimbing,
        mhs=mhs,
        penguji=penguji,
        revisi_terakhir=revisi_terakhir,
        revisi=True,
        **kwargs
    )
    if status:
        sidang["revisi"] = [r for r in sidang["revisi"] if r==status]
    return sidang
