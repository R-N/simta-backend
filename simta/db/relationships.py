from sqlalchemy.orm import relationship
from .Lab import Lab
from .User import User
from .Mahasiswa import Mahasiswa
from .Dosen import Dosen
from .TA import TA
from .Pembimbing import Pembimbing
from .Sidang import Sidang
from .Penguji import Penguji
from .Revisi import Revisi
from .PenolakanRevisi import PenolakanRevisi
from .FormPomits import FormPomits

User.lab = relationship(Lab, backref="members", uselist=False)
#Lab.members = relationship(User)
Mahasiswa.user = relationship(User, uselist=False)
Dosen.user = relationship(User, uselist=False)
TA.mhs = relationship(Mahasiswa, backref="ta", uselist=False)
#Mahasiswa.ta = relationship(TA)
Pembimbing.ta = relationship(TA, backref="pembimbing", uselist=False)
#TA.pembimbing = relationship(Pembimbing)
Pembimbing.dosen = relationship(Dosen, backref="bimbingan", uselist=False)
#Dosen.bimbingan = relationship(Pembimbing)
Sidang.ta = relationship(TA, backref="sidang", uselist=False)
#TA.sidang = relationship(Sidang, uselist=False)
Penguji.sidang = relationship(Sidang, backref="penguji", uselist=False)
#Sidang.penguji = relationship(Penguji)
Penguji.dosen = relationship(Dosen, backref="ujian", uselist=False)
#Dosen.ujian = relationship(Penguji)
Revisi.penguji = relationship(Penguji, backref="revisi", uselist=False)
#Penguji.revisi = relationship(Revisi)
PenolakanRevisi.revisi = relationship(Revisi, backref="penolakan", uselist=False)
#Revisi.penolakan = relationship(PenolakanRevisi, uselist=False)
FormPomits.sidang = relationship(Sidang, backref="form_pomits", uselist=False)
#Sidang.form_pomits = relationship(FormPomits, uselist=False)
