from app import app  # Flask uygulamasını buradan içe aktarın
from app.database import app, create_tables, SessionLocal, Doktor, Randevu, FilmCekim, Sonuc 
import pytest



@pytest.fixture
def client():
    # Flask test istemcisini oluştur
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Test için tabloları oluştur
            create_tables()
        yield client

@pytest.fixture
def setup_database():
    db = SessionLocal()
    try:
        # Tabloları doğru sırayla temizle
        db.query(Sonuc).delete()      # Sonuc tablosunu temizle
        db.query(FilmCekim).delete()  # FilmCekim tablosunu temizle
        db.query(Randevu).delete()   # Randevu tablosunu temizle
        db.query(Doktor).delete()    # Doktor tablosunu temizle
        db.commit()

        # Örnek doktor ekle
        doktor1 = Doktor(ad="Ahmet", soyad="Yılmaz", uzmanlik_alani="Kardiyoloji")
        doktor2 = Doktor(ad="Ayşe", soyad="Demir", uzmanlik_alani="Göz Hastalıkları")
        db.add_all([doktor1, doktor2])
        db.commit()
    finally:
        db.close()

# POST /api/randevu testi
def test_create_randevu(client, setup_database):
    # Geçerli bir randevu oluşturma isteği
    response = client.post('/randevu-ekle', json={
        "doktor_id": 1,
        "hasta_ad": "Betül",
        "hasta_soyad": "Kaya",
        "tarih": "2025-04-28",
        "durum": "DEVAM EDIYOR"
    })
    assert response.status_code == 201
    assert response.json == {"message": "Randevu başarıyla eklendi!"}

