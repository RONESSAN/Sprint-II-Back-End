from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from  model import Base

class Pessoa(Base):
    __tablename__ = 'pessoa'

    id = Column("pk_pessoa", Integer, primary_key=True)
    cpf = Column(String(11), unique=True)
    nome = Column(String(100))
    cep = Column(String(8) )
    logradouro = Column(String(100))
    complemento = Column(String(50) )
    numero = Column(String(20) )
    bairro = Column(String(50))
    cidade = Column(String(100))
    uf = Column(String(2))
    ibge = Column(String(7))
    data_insercao = Column(DateTime, default=datetime.now())    

    def __init__(self, cpf:str, nome:str, cep:str, logradouro:str,
                 complemento:str, numero:str, bairro:str, cidade:str, 
                 uf:str, ibge:str, 
                 data_insercao:Union[DateTime, None] = None):

        self.cpf         = cpf
        self.nome        = nome
        self.cep         = cep
        self.logradouro  = logradouro
        self.complemento = complemento
        self.numero      = numero
        self.bairro      = bairro
        self.cidade      = cidade
        self.uf          = uf
        self.ibge        = ibge

       # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao


