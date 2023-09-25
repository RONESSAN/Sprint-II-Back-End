#from sqlalchemy.ext.declarative import declarative_base   // com a versao nova do sqlalchemy - tive que mudar.
from sqlalchemy.orm import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()
