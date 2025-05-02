from pydantic import BaseModel

class RandevuOlustur(BaseModel):
    hasta_adi: str
    doktor_id: int
    randevu_tarihi: str

# Başka şemalar da eklenebilir