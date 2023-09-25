from sqlalchemy import Column, String, Integer, Float

from model import Base

class Grupo(Base):
    __tablename__ = 'grupo'

    id        = Column("pk_grupo", Integer, primary_key=True)
    descricao = Column(String(100), unique=True)
    margem    = Column(Float)

    def __int__(self, descricao:str, margem:float ):
        """
            Cria um grupo de produtos.
        """
        self.descricao = descricao
        self.margem    = margem
    



