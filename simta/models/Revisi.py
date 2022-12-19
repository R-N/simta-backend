from sqlalchemy import select
from simta.classes import Error
from simta import db, util, models
import os
from flask import send_from_directory
from sqlalchemy.sql import functions as funcs

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

WORKDIR = os.getenv("WORKDIR", "simta")
DIR_FILE_PENOLAKAN = os.path.abspath(f"{WORKDIR}/assets/files/penolakan_revisi")
DIR_FILE_REVISI = os.path.abspath(f"{WORKDIR}/assets/files/revisi")

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

def _get(session, revisi_id, user_id):
    stmt = select(db.Revisi)
    stmt = stmt.filter_by(id=revisi_id)

    revisi = session.scalars(stmt).first()

    if not revisi:
        raise Error("Revisi not found", 404)

    if revisi.penguji.id != user_id and revisi.penguji.sidang.ta.mhs.id != user_id:
        raise Error("Anda tidak berhak mengakses revisi ini", 401)

    return revisi


def get(revisi_id, user_id, sidang=DEFAULT_SIDANG, penguji=DEFAULT_PENGUJI, penolakan=DEFAULT_PENOLAKAN, ta=DEFAULT_TA, pembimbing=DEFAULT_PEMBIMBING, mhs=DEFAULT_MHS, revisi_terakhir=DEFAULT_REVISI_TERAKHIR, **kwargs):
    with db.Session() as session:
        revisi = _get(session, revisi_id, user_id)

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

def terima(revisi_id, penguji_id):
    with db.Session() as session:
        revisi = _get(session, revisi_id, penguji_id)

        if revisi.status != db.RevisiStatus.BARU and revisi.status != db.RevisiStatus.DILIHAT:
            raise Error("Anda sudah menerima/menolak revisi ini", 403)
        
        if revisi.penguji.nilai is None:
            raise Error("Anda belum mengisi nilai", 403)
        
        if revisi.penguji.nomor == 1 and revisi.penguji.sidang.ta.type==db.TAType.TA and revisi.penguji.sidang.ta.mhs.level == db.MhsLevel.S1 and (revisi.penguji.sidang.form_pomits is None or not revisi.penguji.sidang.form_pomits.is_filled):
            raise Error("Anda belum mengisi form POMITS", 403)
        
        if not revisi.penguji.dosen.ttd:
            raise Error("Anda belum upload tanda tangan", 403)

        revisi.status = db.RevisiStatus.DITERIMA
        revisi.updated_at = funcs.now()
        session.add(revisi)

        revisi.penguji.status = db.PengujiStatus.ACC
        session.add(revisi.penguji)

        ta = None
        belum_acc = [1 for p in revisi.penguji.sidang.penguji if p.status!=db.PengujiStatus.ACC]
        if not belum_acc:
            if revisi.penguji.sidang.status != db.SidangStatus.SELESAI:
                revisi.penguji.sidang.status = db.SidangStatus.SELESAI
                session.add(revisi.penguji.sidang)
            if revisi.penguji.sidang.ta.status != db.TAStatus.SELESAI:
                revisi.penguji.sidang.ta.status = db.TAStatus.SELESAI
                session.add(revisi.penguji.sidang.ta)

            if revisi.penguji.sidang.ta.type == db.TAType.PROPOSAL:
                sidang = revisi.penguji.sidang
                ta = db.TA(
                    mhs_id=sidang.ta.mhs.id,
                    judul=sidang.ta.judul,
                    type=db.TAType.TA,
                    status=db.TAStatus.BIMBINGAN
                )
                session.add(ta)
                for p in sidang.ta.pembimbing:
                    p2 = db.Pembimbing(
                        id=p.id,
                        ta=ta,
                        nomor=p.nomor,
                        status=db.PembimbingStatus.BIMBINGAN
                    )
                    session.add(p2)

        session.commit()
        session.flush()

        ret = {}
        if ta:
            ret["ta_id"] = ta.id
        return ret

def tolak(revisi_id, penguji_id, detail, file_name=None):
    with db.Session() as session:
        revisi = _get(session, revisi_id, penguji_id)

        if revisi.status != db.RevisiStatus.BARU and revisi.status != db.RevisiStatus.DILIHAT:
            raise Error("Anda sudah menerima/menolak revisi ini", 403)

        if file_name and not os.path.isfile(os.path.join(DIR_FILE_PENOLAKAN, f"{revisi_id}.pdf")):
            raise Error("Anda belum upload file penolakan", 403)

        if revisi.penolakan:
            revisi.penolakan.detail = detail
            if file_name:
                revisi.penolakan.file_name = file_name
            session.add(revisi.penolakan)
        else:
            penolakan = db.PenolakanRevisi(
                id=revisi.id,
                detail=detail,
                file_name=file_name
            )
            session.add(penolakan)

        revisi.status = db.RevisiStatus.DITOLAK
        revisi.updated_at = funcs.now()
        session.add(revisi)

        session.commit()
        session.flush()


def upload_file_penolakan(revisi_id, file, penguji_id):
    with db.Session() as session:
        revisi = _get(session, revisi_id, penguji_id)

        if revisi.status != db.RevisiStatus.BARU and revisi.status != db.RevisiStatus.DILIHAT:
            raise Error("Anda sudah menerima/menolak revisi ini", 403)

        file.save(f"{DIR_FILE_PENOLAKAN}/{revisi_id}.pdf")

def download_file_penolakan(revisi_id, penguji_id):
    with db.Session() as session:
        revisi = _get(session, revisi_id, penguji_id)

        if revisi.status != db.RevisiStatus.DITOLAK:
            raise Error("Revisi tidak ditolak", 403)

        if not revisi.file_name:
            raise Error("Revisi ditolak tanpa file", 403)

        file_name = f"{revisi_id}.pdf"
        if revisi.file_name and not os.path.isfile(os.path.join(DIR_FILE_PENOLAKAN, file_name)):
            raise Error("File penolakan hilang", 404)

        return send_from_directory(directory=models.Revisi.DIR_FILE_PENOLAKAN, path=file_name, as_attachment=True)

        
def download_file_revisi(revisi_id, penguji_id):
    with db.Session() as session:
        revisi = _get(session, revisi_id, penguji_id)

        file_name = f"{revisi_id}.pdf"
        if revisi.file_name and not os.path.isfile(os.path.join(DIR_FILE_REVISI, file_name)):
            raise Error("File revisi hilang", 404)

        return send_from_directory(directory=models.Revisi.DIR_FILE_REVISI, path=file_name, as_attachment=True)