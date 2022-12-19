from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models


allowed_fields = {
    "id", "mhs_id", "type", "status", "parent_id", "judul"
}
allowed_fields_pembimbing = {"id", "nomor", "status"}
exclude_fields_pembimbing = {"ttd"}
allowed_filters = {"type", "status"}
enums = ["type", "status"]
enums_pembimbing = ["status"]


def join_acc(stmt):
    return stmt.join(
        db.TAAcc,
        (db.TA.id == db.TAAcc.id) & (db.TA.status == db.TAAcc.status),
        isouter=True
    )


def apply_filters(stmt, **kwargs):
    return util.apply_filters(stmt, allowed_filters, kwargs)


DEFAULT_PEMBIMBING = True
DEFAULT_MHS = True
DEFAULT_DOSEN = True


def postprocess(ta, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, dosen=DEFAULT_DOSEN, **kwargs):
    if pembimbing:
        pembimbing = ta.pembimbing
    if mhs:
        mhs = ta.mhs

    ta = util.filter_obj_dict(ta, allowed_fields)
    util.resolve_enums(ta, enums)

    if mhs:
        mhs = models.Mahasiswa.postprocess(mhs)
        ta["mhs"] = mhs

    if pembimbing:
        pembimbing = [{
            **util.filter_obj_dict(p, allowed_fields_pembimbing),
            **(
                util.filter_dict(
                    models.Dosen.postprocess(p.dosen),
                    exclude_fields_pembimbing,
                    False
                ) if dosen else {}
            )
        } for p in pembimbing]
        [util.resolve_enums(p, enums_pembimbing) for p in pembimbing]
        ta["pembimbing"] = pembimbing

    return ta


def get(ta_id, user_id, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, dosen=DEFAULT_DOSEN, **kwargs):
    with db.Session() as session:
        stmt = select(db.TA)
        stmt = stmt.filter_by(id=ta_id)

        ta = session.scalars(stmt).first()

        if not ta:
            raise Error("TA not found", 404)

        if user_id != ta.mhs.id and user_id not in {p.id for p in ta.pembimbing} and not (ta.sidang and user_id in {p.id for p in ta.sidang.penguji}):
            raise Error("Anda tidak berhak mengakses TA ini", 401)

        ta = postprocess(
            ta,
            pembimbing=pembimbing,
            mhs=mhs,
            dosen=dosen,
            **kwargs
        )
    return ta


def _fetch(session, mhs_id=None, pembimbing_id=None, penguji_id=None, **kwargs):
    stmt = select(db.TA)
    if mhs_id:
        stmt = stmt.filter_by(mhs_id=mhs_id)
    if pembimbing_id:
        stmt = stmt.join(
            db.Pembimbing,
            db.Pembimbing.ta_id == db.TA.id,
            isouter=True
        )
    if penguji_id:
        stmt = stmt.join(
            db.Penguji,
            db.Penguji.sidang_id == db.TA.id,
            isouter=True
        )
    if pembimbing_id and penguji_id:
        stmt = stmt.where(
            (db.Pembimbing.id == pembimbing_id)
            | (db.Penguji.id == penguji_id)
        )
    elif pembimbing_id:
        stmt = stmt.where(db.Pembimbing.id == pembimbing_id)
    elif penguji_id:
        stmt = stmt.where(db.Penguji.id == penguji_id)
    stmt = apply_filters(stmt, **kwargs)
    stmt = stmt.distinct()

    ta = session.scalars(stmt).all()

    return ta


def fetch(pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, dosen=DEFAULT_DOSEN, mhs_id=None, pembimbing_id=None, penguji_id=None, **kwargs):
    with db.Session() as session:
        ta = _fetch(
            session,
            mhs_id=mhs_id,
            pembimbing_id=pembimbing_id,
            penguji_id=penguji_id,
            **kwargs
        )
        ta = [postprocess(
            x,
            pembimbing=pembimbing,
            mhs=mhs,
            dosen=dosen,
            **kwargs
        ) for x in ta]
    return ta
