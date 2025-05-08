from fastapi import APIRouter

router = APIRouter()

@router.get("/resepsiyon")
def resepsiyon_bilgi():
    return {"mesaj": "Resepsiyon bilgisi"}