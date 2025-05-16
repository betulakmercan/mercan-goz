from app import app  
from app.database import app, create_tables, SessionLocal, Doktor, Randevu, FilmCekim, Sonuc 
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            create_tables()
        yield client

@pytest.fixture
def setup_database():
    db = SessionLocal()
    try:
        db.query(Sonuc).delete()     
        db.query(FilmCekim).delete()  
        db.query(Randevu).delete()   
        db.query(Doktor).delete()    
        db.commit()

        doktor1 = Doktor(ad="Ahmet", soyad="Gürsoy", uzmanlik_alani="Katarakt Cerrahisi")
        doktor2 = Doktor(ad="Mehmet", soyad="Derman", uzmanlik_alani="Glokom-Katarakt Cerrahisi")
        doktor3 = Doktor(ad="Zeynep", soyad="Akar", uzmanlik_alani="Retina Hastalıkları")
        db.add_all([doktor1, doktor2, doktor3])
        db.commit()
    finally:
        db.close()

#POST/api/randevu testi
def test_create_randevu(client, setup_database):
    response = client.post('/randevu-ekle', json={
        "doktor_id": 1,
        "hasta_ad": "Betül",
        "hasta_soyad": "Kaya",
        "tarih": "2025-04-28",
        "durum": "DEVAM EDIYOR"
    })
    assert response.status_code == 201
    assert response.json == {"message": "Randevu başarıyla eklendi!"}

