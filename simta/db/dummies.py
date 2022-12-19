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

jenis_ta = [
    ("Proposal", TAType.PROPOSAL),
    ("TA", TAType.TA)
]
judul_ta = [
    ("Pembimbing 1", TAStatus.REVISI),
    ("Pembimbing 2, tanpa form POMITS", TAStatus.REVISI),
    ("Penguji 1", TAStatus.REVISI),
    ("Tanpa Hak Akses", TAStatus.REVISI),
    ("Tanpa Sidang", TAStatus.BARU),
    ("Belum Isi POMITS", TAStatus.REVISI),
    ("Belum Isi Nilai", TAStatus.REVISI),
    ("Tanpa POMITS (S2)", TAStatus.REVISI),
    ("Untuk Ditolak 1", TAStatus.REVISI),
    ("Untuk Ditolak 2", TAStatus.REVISI),
    ("Untuk Ditolak 3", TAStatus.REVISI),
    ("Revisi Ditolak", TAStatus.REVISI),
]
Lab.dummies = [
    Lab(
        name="Lab RDIB",
        short="RDIB"
    ),
    Lab(
        name="Lab ADDI",
        short="ADDI"
    )
]
User.dummies = [
    *[
        User(
            name=f"Dosen {i}",
            username=f"dosen{i}",
            password="dosen",
            lab_id=1
        )
        for i in range(1, 1+4)
    ],
    *[
        User(
            name=f"Mahasiswa {1 + len(judul_ta) * i + j}",
            username=f"mhs{1 + len(judul_ta) * i + j}",
            password="dosen",
            lab_id=1
        )
        for i in range(len(jenis_ta))
        for j in range(len(judul_ta))
    ]
]
Dosen.dummies = [
    Dosen(
        id=i,
        nip=f"123{i}",
        ttd=i==1
    )
    for i in range(1, 1+4)
]
Mahasiswa.dummies = [
    Mahasiswa(
        id=1 + 4 + len(judul_ta) * i + j,
        nrp=f"60262210{1 + len(judul_ta) * i + j}",
        level=MhsLevel.S2 if j == 7 else MhsLevel.S1
    )
    for i in range(len(jenis_ta))
    for j in range(len(judul_ta))
]
TA.dummies = [
    TA(
        id=1 + len(judul_ta) * i + j,
        mhs_id=4 + 1 + len(judul_ta) * i + j,
        judul=f"{x[0]} {y[0]}",
        type=x[1],
        status=y[1]
    )
    for i, x in enumerate(jenis_ta)
    for j, y in enumerate(judul_ta)
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
    Pembimbing(
        id=1,
        ta_id=8,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=9,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=10,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=11,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
    Pembimbing(
        id=1,
        ta_id=12,
        nomor=1,
        status=PembimbingStatus.ACC
    ),
]
Pembimbing.dummies = [
    *[
        Pembimbing(
            id=y.id,
            ta_id=y.ta_id + len(judul_ta) * i,
            nomor=y.nomor,
            status=y.status
        )
        for i in range(len(jenis_ta))
        for j, y in enumerate(Pembimbing.dummies)
    ]
]
Sidang.dummies = [
    Sidang(
        id=1 + j + len(judul_ta) * i,
        date=funcs.current_date(),
        start=util.parse_time("08:00"),
        end=util.parse_time("10:00"),
        status=SidangStatus.LULUS
    )
    for i in range(len(jenis_ta))
    for j in range(len(judul_ta)) if j+1 != 5
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
    Penguji(
        id=1,
        sidang_id=8,
        nomor=1,
        status=PengujiStatus.MENGUJI,
        nilai=100
    ),
    Penguji(
        id=1,
        sidang_id=9,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=1,
        sidang_id=10,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=1,
        sidang_id=11,
        nomor=1,
        status=PengujiStatus.MENGUJI
    ),
    Penguji(
        id=1,
        sidang_id=12,
        nomor=1,
        status=PengujiStatus.MENGUJI
    )
]
Penguji.dummies = [
    *[
        Penguji(
            id=y.id,
            sidang_id=y.sidang_id + len(judul_ta) * i,
            nomor=y.nomor,
            status=y.status,
            nilai=y.nilai
        )
        for i in range(len(jenis_ta))
        for j, y in enumerate(Penguji.dummies)
    ]
]
Revisi.dummies = [
    Revisi(
        id=1,
        sidang_id=1,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.DITOLAK,
        created_at=funcs.now(),
        updated_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=2,
        sidang_id=1,
        penguji_id=1,
        nomor=2,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=3,
        sidang_id=2,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=4,
        sidang_id=2,
        penguji_id=2,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=5,
        sidang_id=3,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=6,
        sidang_id=6,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=7,
        sidang_id=7,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=8,
        sidang_id=8,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=9,
        sidang_id=9,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=10,
        sidang_id=10,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=11,
        sidang_id=11,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.BARU,
        created_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
    Revisi(
        id=12,
        sidang_id=12,
        penguji_id=1,
        nomor=1,
        status=RevisiStatus.DITOLAK,
        created_at=funcs.now(),
        updated_at=funcs.now(),
        file_name="asdf.pdf",
        detail=""
    ),
]
Revisi.dummies = [
    *[
        Revisi(
            id=y.id + len(Revisi.dummies) * i,
            sidang_id=y.sidang_id + len(judul_ta) * i,
            penguji_id=y.penguji_id,
            nomor=y.nomor,
            status=y.status,
            created_at=y.created_at,
            file_name=y.file_name,
            detail=y.detail
        )
        for i in range(len(jenis_ta))
        for j, y in enumerate(Revisi.dummies)
    ]
]
PenolakanRevisi.dummies = [
    PenolakanRevisi(
        id=1,
        detail="Metode kurang relevan",
        file_name="rev.pdf"
    ),
    PenolakanRevisi(
        id=12,
        detail="Metode kurang relevan",
        file_name="rev.pdf"
    )
]
PenolakanRevisi.dummies = [
    *[
        PenolakanRevisi(
            id=y.id + len(judul_ta) * i,
            detail=y.detail,
            file_name=y.file_name
        )
        for i in range(len(jenis_ta))
        for j, y in enumerate(PenolakanRevisi.dummies)
    ]
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
        id=6,
    ),
    FormPomits(
        id=7,
        check_1=True,
        check_2=True,
        check_3=False
    ),
]
FormPomits.dummies = [
    *[
        FormPomits(
            id=y.id + len(judul_ta) * i,
            check_1=y.check_1,
            check_2=y.check_2,
            check_3=y.check_3
        )
        for i in range(len(jenis_ta))
        for j, y in enumerate(FormPomits.dummies)
    ]
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