from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from zoneinfo import ZoneInfo


Base = declarative_base()

class Usuario(Base):
    __tablename__= "usuarios"
    id = Column(Integer, primary_key=True)
    nome_completo = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    rg = Column(String, unique=True, nullable=False)
    endereco = Column(String, nullable=False)
    whatsapp = Column(String, unique=True, nullable=False)
    portaria = Column(String, unique=True, nullable=False)
    data_portaria = Column(DateTime, nullable=False)
    data_nascimento = Column(DateTime, nullable=False)
    ativo = Column(Boolean, default=True)

class Agendamento(Base):
    __tablename__= "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    candidato_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    data_agendamento = Column(DateTime, nullable=False)
    criado_em = Column(DateTime, default=lambda: datetime.now(ZoneInfo("America/Sao_Paulo")))
    ativo = Column(Boolean, default=True)

    candidato = relationship("Usuario", backref="agendamentos")