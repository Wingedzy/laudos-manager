from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.models import Base, Usuario, Agendamento
from app.config import engine
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from app.routes import candidatos, agendamento
app = FastAPI()

Base.metadata.create_all(engine)

@app.get("/")
def root ():
    return {"mensagem": "Banco configurado com sucesso!"}


class CandidatoCreate(BaseModel):
    nome_completo: str
    cpf: str
    rg: str 
    endereco: str
    whatsapp: str
    portaria: str
    data_portaria: str
    data_nascimento: str


@app.post("/candidatos/")
def cadastrar_candidato(candidato: CandidatoCreate):
    with Session(engine) as session:
        try:
            data_portaria = datetime.strptime(candidato.data_portaria, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail ="Data inválida, use YYYY-MM-DD")
        
        try:
            data_nascimento = datetime.strptime(candidato.data_nascimento,"%Y-%m-%d" )
        except ValueError:
            raise HTTPException(status_code=400, detail="Data de nascimento inválida")
        
        novo_candidato = Usuario(
            nome_completo=candidato.nome_completo,
            cpf=candidato.cpf,
            rg=candidato.rg,
            endereco=candidato.endereco,
            whatsapp=candidato.whatsapp,
            portaria=candidato.portaria,
            data_portaria=data_portaria,
            data_nascimento=data_nascimento
        )
        
        session.add(novo_candidato)
        session.commit()
        session.refresh(novo_candidato)

        return {
            "id": novo_candidato.id, 
            "mensagem": "Candidato cadastrado com sucesso!", 
            "data_portaria":data_portaria.strftime("%d/%m/%Y")}
    
class AgendamentoCreate(BaseModel):
    candidato_id: int
    data_agendamento: str

@app.post("/agendamentos/")
def cadastrar_agendamento(agendamento: AgendamentoCreate):
    with Session(engine) as session:
        brasilia = ZoneInfo("America/Sao_Paulo")
        try:
            data_agendamento = datetime.strptime(agendamento.data_agendamento, "%Y-%m-%d")
            data_agendamento = data_agendamento.replace(tzinfo=brasilia)
        except ValueError:
            raise HTTPException(status_code=400, detail="Data Inválida, use YYYY-MM-DD")
        
        agora_brasil = datetime.now(brasilia)
        if data_agendamento < agora_brasil + timedelta(hours=72):
            raise HTTPException(status_code=400, detail="Agendamento deve ter pelo menos 72h de antecedência")
        
        candidato= session.get(Usuario, agendamento.candidato_id)
        if not candidato:
            raise  HTTPException(status_code=404, detail= "Candidato não encontrado!")
        
        novo_agendamento = Agendamento (
            candidato_id=agendamento.candidato_id,
            data_agendamento=data_agendamento
        )
        session.add(novo_agendamento)
        session.commit()
        session.refresh(novo_agendamento)

        return {
            "id": novo_agendamento.id,
            "mensagem": f"Agendamento para {candidato.nome_completo} marcado em {data_agendamento.strftime('%d-%m-%Y')}",
            "data_agendamento": data_agendamento.strftime('%d/%m/%Y')
            
            
        }
@app.get("/candidatos/") 
def listar_candidatos():
    with Session(engine) as session:
        candidatos = session.query(Usuario).filter(Usuario.ativo == True).all()
        return [
            {
                "id": c.id,
                "nome_completo": c.nome_completo,
                "cpf": c.cpf,
                "rg": c.rg,
                "data_nascimento": c.data_nascimento.strftime("%d-%m-%Y")
            }
            for c in candidatos
        ] 

@app.get("/agendamentos/") 
def listar_agendamentos():
    with Session(engine) as session:
        agendamentos = session.query(Agendamento).filter(Agendamento.ativo == True).all()
        resultado = []

        for ag in agendamentos:
            candidato = session.get(Usuario, ag.candidato_id)
            resultado.append({
                "id": ag.id,
                "candidato_id": ag.candidato_id,
                "nome_candidato": candidato.nome_completo if candidato else "Não encontrado",
                "data_agendamento": ag.data_agendamento.strftime("%d/%m/%Y")

            })     
        return resultado
        
from fastapi import Path

@app.put("/candidatos/{candidato_id}")
def atualizar_candidato(candidato_id: int, dados: CandidatoCreate):
    with Session(engine) as session:
        candidato = session.get(Usuario, candidato_id)
        if not candidato: 
            raise HTTPException(status_code=404, detail ="Candidato não encontrado!")
        
        try:
            data_portaria = datetime.strptime(dados.data_portaria, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Data inválida, use YYYY-MM-DD")
        
        try: 
            data_nascimento = datetime.strptime(dados.data_nascimento, "%Y-%m-%d"). date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Data de nascimento inválida, use YYYY-MM-DD")

        candidato.nome_completo = dados.nome_completo
        candidato.cpf = dados.cpf
        candidato.rg = dados.rg
        candidato.endereco = dados.endereco
        candidato.whatsapp = dados.whatsapp
        candidato.portaria = dados.portaria
        candidato.data_portaria = data_portaria
        candidato.data_nascimento = data_nascimento

        session.commit()
        session.refresh(candidato)

        return {
            "mensagem": "Candidato atualizado com sucesso!",
            "candidato": {
                "id": candidato.id,
                "nome": candidato.nome_completo,
                "data_portaria": candidato.data_portaria.strftime("%d/%m/%Y")
            }
        }    



app.include_router(candidatos.router)
app.include_router(agendamento.router)

