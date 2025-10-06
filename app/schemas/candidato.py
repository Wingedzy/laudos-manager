from pydantic import BaseModel
from datetime import date

class CandidatoCreate(BaseModel):
    nome_completo: str
    cpf: str
    rg: str
    endereco: str
    whatsapp: str
    portaria: str
    data_portaria: str
    data_nascimento: str


class CandidatoResponse(BaseModel):
    id: int
    nome_completo: str
    cpf: str
    endereco: str
    whatsapp: str
    portaria: str
    data_portaria: str
    data_nascimento: str

    class Config:
        ornm_mode = True