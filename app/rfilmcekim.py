from fastapi import APIRouter

router = APIRouter()

@router.get("/filmcekim")
def film_cekim():
    return {"mesaj": "Film çekimi"}