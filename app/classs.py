from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Doktor(Base):
    __tablename__ = "doktorlar"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    soyad = Column(String, nullable=False)
    uzmanlik = Column(String, nullable=True)

    randevular = relationship("Randevu", back_populates="doktor")

class Randevu(Base):
    __tablename__ = "randevular"

    id = Column(Integer, primary_key=True, index=True)
    hasta_adi = Column(String, nullable=False)
    doktor_id = Column(Integer, ForeignKey("doktorlar.id"))
    tarih = Column(String, nullable=False)
    saat = Column(String, nullable=False)

    doktor = relationship("Doktor", back_populates="randevular")

class Resepsiyon(Base):
    __tablename__ = "resepsiyonlar"

    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String, nullable=False)
    soyad = Column(String, nullable=False)

class FilmCekim(Base):
    __tablename__ = "filmcekimler"

    id = Column(Integer, primary_key=True, index=True)
    randevu_id = Column(Integer, ForeignKey("randevular.id"))
    film_tipi = Column(String, nullable=False)

class Sonuc(Base):
    __tablename__ = "sonuclar"

    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("filmcekimler.id"))
    sonuc_yorumu = Column(String, nullable=False)

