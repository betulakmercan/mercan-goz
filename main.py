from fastapi import FastAPI
from app import database
from app import classs
from app import şemalar
from app import databaseislemler
from app.rdoktor import router as doktor_router
from app.rrandevu import router as randevu_router
from app.rresepsiyon import router as resepsiyon_router
from app.rfilmcekim import router as filmcekim_router
from app.rsonuc import router as sonuc_router


# Veritabanı tabloları oluşturuluyor
classs.Base.metadata.create_all(bind=database.engine)

# FastAPI uygulaması oluşturuluyor
app = FastAPI()
app.include_router(resepsiyon_router)

# Router'ları ekliyoruz
app.include_router(doktor_router)
app.include_router(randevu_router)
app.include_router(filmcekim_router)
app.include_router(sonuc_router)