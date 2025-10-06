from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from app.database import get_db
from app.models import Agendamento, Usuario
from app.schemas.agendamento import AgendamentoCreate, AgendamentoResponse

router = APIRouter(prefix="/agendamentos", tags=["Agendamentos"])

@router.post("/", response_model=AgendamentoResponse)
def cadastrar_agendamento(payload: AgendamentoCreate, db: Session = Depends (get_db)):

    try: 
        brasilia = ZoneInfo("America/Sao_Paulo")
    except ZoneInfoNotFoundError:
        brasilia = None

    try: 
        data_ag = datetime.strptime(payload.data_agendamento, "%Y-%m-%d")
        
        if brasilia:
            data_ag = data_ag.replace(tzinfo=brasilia)
    except ValueError:
        raise HTTPException(status_code=400, detail= "Data inválida, use YYYY-MM-DD")
    
    agora = datetime.now(brasilia) if brasilia else datetime.now()
    if data_ag <agora + timedelta(hours=72):
        raise HTTPException(status_code=400, detail= "agendamento deve ter pelo menos 72h de antecedência")
    
    candidato = db.get(Usuario, payload.candidato_id)
    if not candidato:
        raise HTTPException(status_code=404, detail= "Candidato não encontrado")
    
    novo = Agendamento(candidato_id=payload.candidato_id, data_agendamento= data_ag)
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "id": novo.id,
        "candidato_id": novo.candidato_id,
        "nome_candidato": candidato.nome_completo,
        "data_agendamento": data_ag.strftime("%d/%m/%Y")
    }

@router.get("/{agendamento_id}", response_model=AgendamentoResponse)
def obter_agendamento(agendamento_id: int, db: Session = Depends(get_db)):
    a = db.get(Agendamento, agendamento_id)
    if not a:
        raise HTTPException(status_code=404, detail = "Agendamento não encontrado")
    nome = a.candidato.nome_completo if a.candidato else None

    return {
        "id": a.id,
        "candidato_id": a.candidato_id,
        "nome_candidato": nome,
        "data_agendamento": a.data_agendamento.strftime("%d/%m/%Y") if a.data_agendamento else None
    }

@router.delete ("/{agendamento_id}")
def desativar_agendamento(agendamento_id: int, db: Session = Depends (get_db)):
    ag = db.get(Agendamento, agendamento_id)
    if not ag:
        raise HTTPException(status_code=404, detail= "Agendamento não encontrado")
    
    ag.ativo = False
    db.commit()
    db.refresh(ag)

    return {"mensagem": "Agendamento desativado com sucesso"}