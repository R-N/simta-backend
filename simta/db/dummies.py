from .Lab import Lab
from .User import User
from .Mahasiswa import Mahasiswa, MhsLevel
from .Dosen import Dosen
from .TA import TA, TAType, TAStatus
from .Pembimbing import Pembimbing, PembimbingStatus
from .Sidang import Sidang, SidangStatus
from .Penguji import Penguji, PengujiStatus
from .Revisi import Revisi, RevisiStatus
from .PenolakanRevisi import PenolakanRevisi
from .FormPomits import FormPomits
from sqlalchemy.sql import functions as funcs
from simta import util

Lab.dummies = [
    Lab(
        name="RDIB",
        short="RDIB"
    ),
    Lab(
        name="ADDI",
        short="ADDI"
    )
]
User.dummies = [
    User(
        name="Dosen Satu",
        username="dosen1",
        password="dosen",
        lab_id=1
    ),
    User(
        name="Dosen Dua",
        username="dosen2",
        password="dosen",
        lab_id=1
    ),
    User(
        name="Dosen Tiga",
        username="dosen3",
        password="dosen",
        lab_id=1
    ),
    User(
        name="Dosen Empat",
        username="dosen4",
        password="dosen",
        lab_id=1
    ),
    User(
        name="Mahasiswa Satu",
        username="mhs1",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Dua",
        username="mhs2",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Tiga",
        username="mhs3",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Empat",
        username="mhs4",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Lima",
        username="mhs5",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Enam",
        username="mhs6",
        password="mhs",
        lab_id=1
    ),
    User(
        name="Mahasiswa Tujuh",
        username="mhs7",
        password="mhs",
        lab_id=1
    ),
]
Dosen.dummies = [
    Dosen(
        id=1,
        nip="1231",
        ttd=True
    ),
    Dosen(
        id=2,
        nip="1232"
    ),
    Dosen(
        id=3,
        nip="1233"
    ),
    Dosen(
        id=4,
        nip="1234"
    )
]
Mahasiswa.dummies = [
    Mahasiswa(
        id=5,
        nrp="6026221001",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=6,
        nrp="6026221002",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=7,
        nrp="6026221003",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=8,
        nrp="6026221004",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=9,
        nrp="6026221005",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=10,
        nrp="6026221006",
        level=MhsLevel.S1
    ),
    Mahasiswa(
        id=11,
        nrp="6026221007",
        level=MhsLevel.S1
    ),
]
TA.dummies = [
    TA(
        mhs_id=5,
        judul="Proposal Pembimbing 1",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
    TA(
        mhs_id=6,
        judul="Proposal Pembimbing 2, tanpa form POMITS",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
    TA(
        mhs_id=7,
        judul="Proposal Penguji 1",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
    TA(
        mhs_id=8,
        judul="Proposal Tanpa Hak Akses",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
    TA(
        mhs_id=9,
        judul="Proposal Tanpa Sidang",
        type=TAType.PROPOSAL,
        status=TAStatus.BARU
    ),
    TA(
        mhs_id=10,
        judul="Proposal Belum Isi POMITS",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
    TA(
        mhs_id=11,
        judul="Proposal Belum Isi Nilai",
        type=TAType.PROPOSAL,
        status=TAStatus.REVISI
    ),
]
Pembimbing.dummies = [
    Pembimbing(
        id=1,
        ta_id=1,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=2,
        ta_id=2,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=2,
        nomor=2,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=2,
        ta_id=3,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=5,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=6,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=7,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
]
Sidang.dummies = [
    Sidang(
        id=1,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
    Sidang(
        id=2,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
    Sidang(
        id=3,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
    Sidang(
        id=4,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
    Sidang(
        id=6,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
    Sidang(
        id=7,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    ),
]
Penguji.dummies = [
    Penguji(
        id=1,
        sidang_id=1,
        nomor=1,
        status=PengujiStatus.MENGUJI,
        nilai=100
    ),
    Penguji(
        id=2,
        sidang_id=2,
        nomor=1,
        status=PengujiStatus.MENGUJI,
        nilai=100
    ),
    Penguji(
        id=1,
        sidang_id=2,
        nomor=2,
        status=PengujiStatus.MENGUJI,
        nilai=100
    ),
    Penguji(
        id=1,
        sidang_id=3,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=2,
        sidang_id=3,
        nomor=2,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=2,
        sidang_id=4,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=1,
        sidang_id=6,
        nomor=1,
        status=PengujiStatus.MENGUJI,
        nilai=100
    ),
    Penguji(
        id=1,
        sidang_id=7,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
]
Revisi.dummies = [
    Revisi(
        sidang_id=1,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.DITOLAK,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=1,
        penguji_id=1,
        nomor=2,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=2,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=2,
        penguji_id=2,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=3,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=6,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        sidang_id=7,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
]
PenolakanRevisi.dummies = [
    PenolakanRevisi(
        id=1,
        detail="Metode kurang relevan",
        file_name="rev.pdf"
    )
]
FormPomits.dummies = [
    FormPomits(
        id=1,
        check_1=True,
        check_2=True,
        check_3=False
    ),
    FormPomits(
        id=2,
        check_1=True,
        check_2=True,
        check_3=False
    ),
    FormPomits(
        id=4,
        check_1=True,
        check_2=True,
        check_3=False
    ),
    FormPomits(
        id=7,
        check_1=True,
        check_2=True,
        check_3=False
    ),
]

dummies = [
    *Lab.dummies,
    *User.dummies,
    *Dosen.dummies,
    *Mahasiswa.dummies,
    *TA.dummies,
    *Pembimbing.dummies,
    *Sidang.dummies,
    *Penguji.dummies,
    *Revisi.dummies,
    *PenolakanRevisi.dummies,
    *FormPomits.dummies
]