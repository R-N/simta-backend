from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models


allowed_fields = {
    "id", "date", "start", "end", "status"
}
allowed_fields_penguji = {"id", "nomor", "status", "catatan_revisi", "nilai", "revisi_terakhir"}
exclude_fields_penguji = {"ttd", "revisi"}
allowed_filters = {"type", "status"}
enums = ["status"]
strs = ["date", "start", "end"]
enums_penguji = ["status"]

DEFAULT_USER_ID = None
DEFAULT_PENGUJI = True
DEFAULT_TA = True
DEFAULT_PEMBIMBING = True
DEFAULT_REVISI_TERAKHIR = True
DEFAULT_MHS = True
DEFAULT_PEMBIMBING_DOSEN = False
DEFAULT_REVISI = False


def apply_filters(stmt, **kwargs):
    return util.apply_filters(stmt, allowed_filters, kwargs)


def postprocess(sidang, user_id=DEFAULT_USER_ID, penguji=DEFAULT_PENGUJI, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, mhs=DEFAULT_MHS, pembimbing_dosen=DEFAULT_PEMBIMBING_DOSEN, revisi=DEFAULT_REVISI, **kwargs):
    if ta:
        ta = sidang.ta
    if penguji or (user_id and (revisi_terakhir or revisi)):
        _penguji = sidang.penguji
        if penguji:
            penguji = _penguji

    sidang = util.filter_obj_dict(sidang, allowed_fields)
    util.resolve_enums(sidang, enums)
    util.resolve_strs(sidang, strs)

    if ta:
        sidang["ta"] = models.TA.postprocess(ta, pembimbing=pembimbing, mhs=mhs, dosen=pembimbing_dosen, **kwargs)
    if user_id and (revisi_terakhir or revisi):
        me = [p for p in _penguji if p.id == user_id]
        me = me[0] if me else None
        if me:
            if revisi_terakhir:
                revisi_terakhir = sorted(me.revisi, key=lambda x: x.nomor)[-1]
                revisi_terakhir = models.Revisi.postprocess(revisi_terakhir, sidang=False)
            if revisi:
                revisi = me.revisi
                revisi = [models.Revisi.postprocess(r, sidang=False) for r in revisi]
        else:
            revisi_terakhir = None

    if penguji:
        penguji = [{
            **util.filter_obj_dict(p, allowed_fields_penguji),
            **util.filter_dict(
                models.Dosen.postprocess(p.dosen),
                exclude_fields_penguji,
                False
            )
        } for p in penguji]
        [util.resolve_enums(p, enums_penguji) for p in penguji]
        sidang["penguji"] = penguji

    if user_id and revisi_terakhir:
        sidang["revisi_terakhir"] = revisi_terakhir
    if user_id and revisi:
        sidang["revisi"] = revisi

    return sidang

def _get(session, sidang_id):
    stmt = select(db.Sidang)
    stmt = stmt.filter_by(id=sidang_id)

    sidang = session.scalars(stmt).first()

    if not sidang:
        raise Error("Sidang not found", 404)

    return sidang


def get(sidang_id, user_id=DEFAULT_USER_ID, penguji=DEFAULT_PENGUJI, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, mhs=DEFAULT_MHS, pembimbing_dosen=DEFAULT_PEMBIMBING_DOSEN, revisi=DEFAULT_REVISI, **kwargs):
    with db.Session() as session:
        sidang = _get(session, sidang_id)

        sidang = postprocess(
            sidang,
            user_id=user_id,
            penguji=penguji,
            ta=ta,
            pembimbing=pembimbing,
            revisi_terakhir=revisi_terakhir,
            mhs=mhs,
            pembimbing_dosen=pembimbing_dosen,
            revisi=revisi,
            **kwargs
        )
    return sidang

def fetch(user_id=DEFAULT_USER_ID, penguji=DEFAULT_PENGUJI, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, mhs=DEFAULT_MHS, pembimbing_dosen=DEFAULT_PEMBIMBING_DOSEN, revisi=DEFAULT_REVISI, status=None, ta_status=None, ta_type=None, **kwargs):
    if ta_status:
        kwargs["status"] = ta_status
        kwargs["type"] = ta_type

    with db.Session() as session:
        _ta = models.TA._fetch(
            session,
            **kwargs
        )
        sidang = [t.sidang for t in _ta]
        if status:
            sidang = [s for s in sidang if s.status == status]
        sidang = [postprocess(
            t,
            user_id=user_id,
            penguji=penguji,
            ta=ta,
            pembimbing=pembimbing,
            revisi_terakhir=revisi_terakhir,
            mhs=mhs,
            pembimbing_dosen=pembimbing_dosen,
            revisi=revisi,
            **kwargs
        ) for t in sidang]
    return sidang
