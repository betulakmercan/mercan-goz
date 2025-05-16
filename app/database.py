from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from urllib.parse import quote_plus
from flask import Flask, jsonify, request

Base = declarative_base()
app = Flask(__name__)

password = quote_plus("betul24")
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://betul:{password}@localhost:3306/project1"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Doktor(Base):
    __tablename__ = "doktor"
    id = Column(Integer, primary_key=True, index=True)
    ad = Column(String(50), nullable=False)
    soyad = Column(String(50), nullable=False)
    uzmanlik_alani = Column(String(100), nullable=False)

    randevular = relationship("Randevu", back_populates="doktor")
class Randevu(Base):
    __tablename__ = "randevu"
    id = Column(Integer, primary_key=True, index=True)
    doktor_id = Column(Integer, ForeignKey("doktor.id", ondelete="CASCADE"), nullable=False)
    hasta_ad = Column(String(50), nullable=False)
    hasta_soyad = Column(String(50), nullable=False)
    tarih = Column(Date, nullable=False)
    durum = Column(String(50), nullable=False)

    doktor = relationship("Doktor", back_populates="randevular")

class FilmCekim(Base):
    __tablename__ = "filmcekimler"
    id = Column(Integer, primary_key=True, index=True)
    randevu_id = Column(Integer, ForeignKey("randevu.id", ondelete="CASCADE"), nullable=False)
    film_tipi = Column(String(50), nullable=False)

class Sonuc(Base):
    __tablename__ = "sonuclar"
    id = Column(Integer, primary_key=True, index=True)
    film_id = Column(Integer, ForeignKey("filmcekimler.id"))
    sonuc_yorumu = Column(String(50), nullable=False)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablolar oluşturuldu!")
    except Exception as e:
        print(f"Tablo oluşturma hatası: {e}")
#veritabanı bağlantısı
def check_database_connection():
    try:
        connection = engine.connect()
        print("Veritabanı bağlantısı başarılı!")
        connection.close()
    except Exception as e:
        print(f"Veritabanı bağlantı hatası: {e}")


def add_doktor(ad, soyad, uzmanlik_alani):
    db = SessionLocal()
    try:
        mevcut_doktor = db.query(Doktor).filter(
            Doktor.ad == ad,
            Doktor.soyad == soyad,
            Doktor.uzmanlik_alani == uzmanlik_alani
        ).first()
        if mevcut_doktor:
            print(f"Doktor zaten mevcut: {mevcut_doktor.ad} {mevcut_doktor.soyad}")
            return

        yeni_doktor = Doktor(ad=ad, soyad=soyad, uzmanlik_alani=uzmanlik_alani)
        db.add(yeni_doktor)
        db.commit()
        print(f"Doktor eklendi: {yeni_doktor.ad} {yeni_doktor.soyad}")
    except Exception as e:
        print(f"Doktor ekleme hatası: {e}")
    finally:
        db.close()


def add_randevu(doktor_id, hasta_ad, hasta_soyad, tarih, durum):
    db = SessionLocal()
    try:
        # Aynı randevunun zaten mevcut olup olmadığını kontrol et
        mevcut_randevu = db.query(Randevu).filter(
            Randevu.doktor_id == doktor_id,
            Randevu.hasta_ad == hasta_ad,
            Randevu.hasta_soyad == hasta_soyad,
            Randevu.tarih == tarih
        ).first()

        if mevcut_randevu:
            print(f"Randevu zaten mevcut: {mevcut_randevu.hasta_ad} {mevcut_randevu.hasta_soyad}, Tarih: {mevcut_randevu.tarih}")
            return

        yeni_randevu = Randevu(
            doktor_id=doktor_id,
            hasta_ad=hasta_ad,
            hasta_soyad=hasta_soyad,
            tarih=tarih,
            durum=durum
        )
        db.add(yeni_randevu)
        db.commit()
        print(f"Randevu eklendi: Hasta {hasta_ad} {hasta_soyad}, Tarih: {tarih}")
    except Exception as e:
        print(f"Randevu ekleme hatası: {e}")
    finally:
        db.close()


def get_all_doktor():
    db = SessionLocal()
    try:
        doktorlar = db.query(Doktor).all()
        for doktor in doktorlar:
            print(f"ID: {doktor.id}, Ad: {doktor.ad}, Soyad: {doktor.soyad}, Uzmanlık: {doktor.uzmanlik_alani}")
    except Exception as e:
        print(f"Doktorları listeleme hatası: {e}")
    finally:
        db.close()

@app.route('/api/randevular', methods=['GET'])
def get_randevular():
    db = SessionLocal()
    try:
        randevular = db.query(Randevu).all()
        randevu_listesi = [
            {
                "id": randevu.id,
                "doktor_id": randevu.doktor_id,
                "hasta_ad": randevu.hasta_ad,
                "hasta_soyad": randevu.hasta_soyad,
                "tarih": str(randevu.tarih),
                "durum": randevu.durum
            }
            for randevu in randevular
        ]
        return jsonify(randevu_listesi), 200
    except Exception as e:
        return jsonify({"error": f"Randevuları listeleme hatası: {str(e)}"}), 500
    finally:
        db.close()

@app.route('/randevu-ekle', methods=['POST'])
def randevu_ekle():
    data = request.json
    doktor_id = data.get('doktor_id')
    hasta_ad = data.get('hasta_ad')
    hasta_soyad = data.get('hasta_soyad')
    tarih = data.get('tarih')
    durum = data.get('durum', 'Beklemede')

    if not doktor_id or not hasta_ad or not hasta_soyad or not tarih:
        return jsonify({"error": "Eksik bilgi. Lütfen tüm alanları doldurun."}), 400

    try:
        add_randevu(doktor_id, hasta_ad, hasta_soyad, tarih, durum)
        return jsonify({"message": "Randevu başarıyla eklendi!"}), 201
    except Exception as e:
        return jsonify({"error": f"Randevu ekleme hatası: {str(e)}"}), 500

def get_all_randevu():
    db = SessionLocal()
    try:
        randevular = db.query(Randevu).all()
        for randevu in randevular:
            print(f"ID: {randevu.id}, Doktor ID: {randevu.doktor_id}, Hasta: {randevu.hasta_ad} {randevu.hasta_soyad}, Tarih: {randevu.tarih}, Durum: {randevu.durum}")
    except Exception as e:
        print(f"Randevuları listeleme hatası: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_database_connection()
    create_tables()

    if not SessionLocal().query(Doktor).first():
        add_doktor("Prof. Dr. Ahmet", "Gürsoy", "Katarakt Cerrahisi")
        add_doktor("Doç. Dr. Zeynep", "Akar", "Retina Hastalıkları")
        add_doktor("Dr. Öğr. Üyesi Mehmet", "Derman", "Glokom-Katarakt Cerrahisi")

    if not SessionLocal().query(Randevu).first():
        add_randevu(1, "Ece", "Demir", "2025-04-28", "Onaylandı")
        add_randevu(2, "Ali", "Yıldız", "2025-08-22", "Beklemede")
        add_randevu(3, "Betül", "Akmercan", "2025-05-03", "Sonuçlandı")

    print("\n--- Doktor Tablosu ---")
    get_all_doktor()

    print("\n--- Randevu Tablosu ---")
    get_all_randevu()

    app.run(debug=False)


