from sqlalchemy import Column, String, Integer
from model import Base

class Marca(Base):
    __tablename__ = 'marca'

    id        = Column("pk_marca", Integer, primary_key=True)
    descricao = Column(String(100), unique=True)

    def __int__(self, descricao:str ):
        """
            Cria um marca de produtos.
        """
        self.descricao = descricao
    



