from fastapi import APIRouter

router = APIRouter()

@router.get("/sonuclar")
def sonuclari_getir():
    return {"mesaj": "Sonuçlar"}
