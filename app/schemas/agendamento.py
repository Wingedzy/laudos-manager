from pydantic import BaseModel

class AgendamentoCreate(BaseModel):
    candidato_id: int
    data_agendamento: str

class AgendamentoResponse(BaseModel):
    id: int
    candidato_id: int
    nome_candidato: str
    data_agendamento: str

    class Config:
        orm_mode = True