from fastapi import APIRouter

router = APIRouter()

@router.get("/doktorlar")
def doktorlari_getir():
    return {"mesaj": "Doktorlar listesi"}