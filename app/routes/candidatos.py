from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.models import Usuario
from app.schemas.candidato import CandidatoCreate, CandidatoResponse


router = APIRouter(prefix="/candidatos", tags = ["Candidatos"])

@router.post("/", response_model=CandidatoResponse)
def cadastrar_candidato(candidato: CandidatoCreate, db: Session = Depends(get_db)):
    try: 
        data_portaria = datetime.strptime(candidato.data_portaria, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail = "Data inválida, use YYYY-MM-DD")
    
    try: 
        data_nascimento = datetime.strptime(candidato.data_nascimento, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail = "Data de nascimento inválida, use YYYY-MM-DD")
    
    
    novo = Usuario(
        nome_completo = candidato.nome_completo,
        cpf = candidato.cpf,
        rg = candidato.rg,
        endereco = candidato.endereco,
        whatsapp = candidato.whatsapp,
        portaria = candidato.portaria,
        data_portaria = data_portaria,
        data_nascimento = candidato.data_nascimento
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)

    return {
        "id": novo.id,
        "nome_completo": novo.nome_completo,
        "cpf": novo.cpf,
        "rg": novo.rg,
        "endereco": novo.endereco,
        "whatsapp": novo.whatsapp,
        "portaria": novo.portaria,
        "data_portaria": data_portaria.strftime("%d/%m/%Y"),
        "data_nascimento":data_nascimento.strftime("%d/%m/%Y"),
    }


@router.get("/", response_model=list[CandidatoResponse])
def listar_candidatos(db: Session = Depends(get_db)):
    candidatos = db.query(Usuario).filter(Usuario.ativo == True). all()
    resultado = []
    for c in candidatos: 
        resultado.append({
            "id": c.id,
            "nome_completo": c.nome_completo,
            "cpf": c.cpf,
            "rg": c.rg,
            "endereco": c.endereco,
            "whatsapp": c.whatsapp,
            "portaria": c.portaria,
            "data_portaria": c.data_portaria.strftime("%d/%m/%Y") if c.data_portaria else None,
            "data_nascimento": c.data_nascimento.strftime("%d/%m/%Y") if c.data_nascimento else None
        })
    return resultado


@router.get("/{candidato_id}", response_model=CandidatoResponse)
def obter_candidato(candidato_id: int, db: Session = Depends(get_db)):
    c = db.get(Usuario, candidato_id)
    if not c:
        raise HTTPException(status_code=404, detail = "Candidato não encontrado")
    return{
        "id": c.id,
        "nome_completo":c.nome_completo,
        "cpf": c.cpf,
        "rg": c.rg,
        "endereco": c.endereco,
        "whatsapp": c.whatsapp,
        "portaria": c.portaria,
        "data_portaria": c.data_portaria.strftime("%d/%m/%Y") if c.data_portaria else None,
        "data_nascimento": c.data_nascimento.strftime("%d/%m/%Y") if c.data_nascimento else None,
    }
  
@router.put("/{candidato_id}", response_model=CandidatoResponse)
def atualizar_candidato(candidato_id: int, dados: CandidatoCreate, db: Session = Depends(get_db)):
  c = db.get(Usuario, candidato_id)
  if not c:
      raise HTTPException(status_code=404, detail="Candidato não encontrado")
  try:
      data_portaria = datetime.strptime(dados.data_portaria, "%Y-%m-%d" )
  except ValueError:
      raise HTTPException(status_code=400, detail ="Data inválida, use YYYY-MM-DD")
  
  try:
      data_nascimento = datetime.strptime(dados.data_nascimento, "%Y-%m-%d" )
  except ValueError:
      raise HTTPException(status_code=400, detail ="Data de nascimento inválida, use YYYY-MM-DD")
 
  c.nome_completo = dados.nome_completo
  c.cpf = dados.cpf
  c.rg = dados.rg
  c.endereco = dados.endereco
  c.whatsapp = dados.whatsapp
  c.portaria = dados.portaria
  c.data_portaria = data_portaria
  c.data_nascimento = dados.data_nascimento

  db.commit()
  db.refresh(c)

  return{
    "id": c.id,
    "nome_completo": c.nome_completo,
    "cpf": c.cpf,
    "rg": c.rg,
    "endereco": c.endereco,
    "whatsapp": c.whatsapp,
    "portaria": c.portaria,
    "data_portaria": c.data_portaria.strftime ("%d/%m/%Y"),
    "data_nascimento": c.data_nascimento.strftime ("%d/%m/%Y")
}

@router.delete("/{candidato_id}")
def desativar_candidato(candidato_id: int, db: Session = Depends(get_db)):
    c = db.get(Usuario, candidato_id)
    if not c:
        raise HTTPException(status_code=404, detail = "Candidato não encontrado")
    
    c.ativo = False
    db.commit()
    db.refresh(c)

    return {"mensagem": f"Candidato {c.nome_completo} desativado com sucesso!"}












   