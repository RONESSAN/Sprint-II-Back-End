from pydantic import BaseModel, validator
from typing import Optional, List   
from model.usuario import Usuario
from model.produto import Produto
from model.pessoa import Pessoa
from model.marca import Marca
from model.grupo import Grupo
from datetime import date
from datetime import datetime
import re

"""
   schema - usuario
"""
class UsuarioSchema(BaseModel):
    """ Define como um novo usuario a ser inserido dever ser representado
    """
    nome: str = "RONES MENDONCA"
    email: str = "rones@rmsys.net"
    senha: str = "123456"

class UpdateUsuarioSchema(BaseModel):
    """ Define como um email pode ser atualizado.
    """
    id : int = 1
    nome: str = "RONES MENDONCA"
    email: str = "rones@rmsys.net"

class UsuarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id o usuario.
    """    
    usuario_id: int = 1


class UsuarioValidaLoginSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no email e senha do usuario.
    """    
    email: str = "rones@rmsys.net"
    senha: str = "123456"


class ListagemUsuariosSchema(BaseModel):
    """ Define como uma listagem de usuarios será retornada.
    """
    usuarios:List[UsuarioSchema]   


def apresenta_usuarios(usuarios: List[Usuario] ):
    """ Retorna uma representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    result=[]
    for usuario in usuarios:        
        result.append({
               "id": usuario.id,
             "nome": usuario.nome,
            "email": usuario.email,
        })

    return {"usuarios": result}


class UsuarioViewSchema(BaseModel):
    """ Define como um usuario será retornado.
    """
    email: str = "rones@rmsys.net"
    senha: str = "123456"


class UsuarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição de remoção.
    """
    message: str
    email: str

def apresenta_usuario(usuario: Usuario):
    """ Retorna um representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    return {
           "id": usuario.id,
         "nome": usuario.nome,
        "email": usuario.email,
    }

def apresenta_login(usuario: Usuario):
    """ Retorna um representação do usuario seguindo o schema definido em 
        UsuarioViewSchema.
    """
    return {
        "email": usuario.email,
        "senha": usuario.senha,
    }

"""
   schema - produto
"""

class ProdutoSchema(BaseModel):
    """ Define como um novo produto a ser inserido deve ser representado
    """
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    data_validade: str = "25/12/2023"

    @validator('data_validade')
    def valida_data_validade(cls, v):
        if re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", v):
            return v

        raise ValueError('A data tem que ser no formato dd/mm/aaaa')    


class UpdateProdutoSchema(BaseModel):
    """ Define como um novo produto pode ser atualizado.
    """
    id : int = 1
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: Optional[float] = 12.50
    data_validade: Optional[str] = "25/12/2023"


class ProdutoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do produto.
    """
    produto_id: int = 1


class ListagemProdutosSchema(BaseModel):
    """ Define como uma listagem de produtos será retornada.
    """
    produtos:List[ProdutoSchema]


def apresenta_produtos(produtos: List[Produto]):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for produto in produtos:
        result.append({
            "id": produto.id,
            "nome": produto.nome,
            "quantidade": produto.quantidade,
            "valor": produto.valor,
            "data_validade": datetime.strftime(produto.data_validade, '%d/%m/%Y')            
        })

    return {"produtos": result}


class ProdutoViewSchema(BaseModel):
    """ Define como um produto será retornado: produto.
    """
    id: int = 1
    nome: str = "BANANA PRATA"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    data_validade: str = "25/12/2023"    


class ProdutoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_produto(produto: Produto):
    """ Retorna uma representação do produto seguindo o schema definido em
        ProdutoViewSchema.
    """
    return {
        "id": produto.id,
        "nome": produto.nome,
        "quantidade": produto.quantidade,
        "valor": produto.valor,
        "data_validade": datetime.strftime(produto.data_validade, '%d/%m/%Y')        
    }

"""
   schema - pessoa
"""

class PessoaSchema(BaseModel):
    """ Define como um nova pessoa a ser inserido deve ser representado
    """
    cpf: str = "059.979.360-07"
    nome: str = "RONES MENDONCA DOS SANTOS"
    cep: str = "75.530-370"
    logradouro: str = "RUA JOAO RODRIGUES JOTA"
    complemento: str = "A"
    numero: str = "1191"
    bairro: str = "SANTOS DUMONT"
    cidade: str = "ITUMBIARA"
    uf: str = "GO"
    ibge: str = "5211503"


class UpdatePessoaSchema(BaseModel):
    """ Define como um nova pessoa pode ser atualizado.
    """
    id : int = 1
    cpf: str = "059.979.360-07"
    nome: str = "RONES MENDONCA DOS SANTOS"
    cep: str = "75.530-370"
    logradouro: str = "RUA JOAO RODRIGUES JOTA"
    complemento: str = "A"
    numero: str = "1191"
    bairro: str = "SANTOS DUMONT"
    cidade: str = "ITUMBIARA"
    uf: str = "GO"
    ibge: str = "5211503"


class PessoaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da pessoa.
    """
    pessoa_id: int = 1


class ListagemPessoasSchema(BaseModel):
    """ Define como uma listagem de pessoas será retornada.
    """
    pessoas:List[PessoaSchema]


class PessoaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

class PessoaViewSchema(BaseModel):
    """ Define como uma pessoa será retornada.
    """    
    id : int = 1
    cpf: str = "059.979.360-07"
    nome: str = "RONES MENDONCA DOS SANTOS"
    cep: str = "75.530-370"
    logradouro: str = "RUA JOAO RODRIGUES JOTA"
    complemento: str = "A"
    numero: str = "1191"
    bairro: str = "SANTOS DUMONT"
    cidade: str = "ITUMBIARA"
    uf: str = "GO"
    ibge: str = "5211503"


def apresenta_pessoas(pessoas: List[Pessoa]):
    """ Retorna uma representação de pessoas seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for pessoa in pessoas:
        result.append({
            "id": pessoa.id,
            "cpf": pessoa.cpf,
            "nome": pessoa.nome,
            "cep": pessoa.cep,
            "logradouro": pessoa.logradouro,
            "complemento": pessoa.complemento,
            "numero": pessoa.numero,
            "bairro": pessoa.bairro,
            "cidade": pessoa.cidade,
            "uf": pessoa.uf,
            "ibge": pessoa.ibge
        })

    return {"pessoas": result}

def apresenta_pessoa(pessoa: Pessoa):
    """ Retorna uma representação da pessoa seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": pessoa.id,
        "cpf": pessoa.cpf,
        "nome": pessoa.nome,
        "cep": pessoa.cep,
        "logradouro": pessoa.logradouro,
        "complemento": pessoa.complemento,
        "numero": pessoa.numero,
        "bairro": pessoa.bairro,
        "cidade": pessoa.cidade,
        "uf": pessoa.uf,
        "ibge": pessoa.ibge        
    }

"""
   schema - marca
"""

class MarcaSchema(BaseModel):
    """ Define como uma nova marca a ser inserida deve ser representada
    """
    descricao: str = "TIGRE"


class UpdateMarcaSchema(BaseModel):
    """ Define como uma nova marca pode ser atualizada
    """
    id : int = 1
    descricao: str = "TIGRE"


class MarcaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id da marca.
    """
    marca_id: int = 1


class ListagemMarcasSchema(BaseModel):
    """ Define como uma listagem de marcas será retornada.
    """
    marcas:List[MarcaSchema]


class MarcaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

class MarcaViewSchema(BaseModel):
    """ Define como uma marca será retornada.
    """    
    id : int = 1
    descricao: str = "TIGRE"

def apresenta_marcas(marcas: List[Marca]):
    """ Retorna uma representação de marcas seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for marca in marcas:
        result.append({
            "id": marca.id,
            "descricao": marca.descricao
        })

    return {"marcas": result}

def apresenta_marca(marca: Marca):
    """ Retorna uma representação de grupo seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": marca.id,
        "descricao": marca.descricao
    }

"""
   schema - grupo
"""

class GrupoSchema(BaseModel):
    """ Define como um novo grupo a ser inserido deve ser representado
    """
    descricao: str = "FERRAMENTAS"
    margem: float = 30.00


class UpdateGrupoSchema(BaseModel):
    """ Define como um novo grupo pode ser atualizado.
    """
    id : int = 1
    descricao: str = "FERRAMENTAS"
    margem: float = 30.00


class GrupoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no id do grupo.
    """
    grupo_id: int = 1


class ListagemGruposSchema(BaseModel):
    """ Define como uma listagem de grupos será retornada.
    """
    grupos:List[GrupoSchema]


class GrupoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    descricao: str

class GrupoViewSchema(BaseModel):
    """ Define como um grupo será retornado.
    """    
    id : int = 1
    descricao: str = "FERRAMENTAS"
    margem: float = 30.00

def apresenta_grupos(grupos: List[Grupo]):
    """ Retorna uma representação de grupos seguindo o schema definido em
        PessoaViewSchema.
    """
    result = []
    for grupo in grupos:
        result.append({
            "id": grupo.id,
            "descricao": grupo.descricao,
            "margem": grupo.margem
        })

    return {"grupos": result}

def apresenta_grupo(grupo: Grupo):
    """ Retorna uma representação de grupo seguindo o schema definido em
        PessoaViewSchema.
    """
    return {
        "id": grupo.id,
        "descricao": grupo.descricao,
        "margem": grupo.margem
    }
