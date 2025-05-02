from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import database, şemalar, databaseislemler

router = APIRouter()

@router.post("/randevu-ekle")
def randevu_ekle(veri: şemalar.RandevuOlustur, db: Session = Depends(database.SessionLocal)):
    return databaseislemler.randevu_olustur(db, veri)