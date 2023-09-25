from operator import and_
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
import base64

from model import Session, Produto, Usuario, Pessoa, Grupo, Marca
from schemas import *

from datetime import datetime

info = Info(title="Gescom WEB", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
gescom_tag = Tag(name="Gescom", description="Adição, visualização, alteração e remoção de usuario/produto/pessoa/grupo e marca à base")
                  
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/produto', tags=[gescom_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_produto(form: ProdutoSchema):
    """Adiciona um novo Produto à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    produto = Produto(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor,
        data_validade=datetime.strptime(form.data_validade, '%d/%m/%Y') 
    )    

    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(produto)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        return apresenta_produto(produto), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400


@app.post('/update_produto', tags=[gescom_tag],
          responses={"200": ProdutoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_produto(form: UpdateProdutoSchema):
    """Edita um Produto já salvo na base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    id_prod = form.id
    session = Session()
    
    try:
        query = session.query(Produto).filter(Produto.id == id_prod)
        db_produto = query.first()
        if not db_produto:
            # se o produto não foi encontrado
            error_msg = "Produto não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.nome:
                db_produto.nome = form.nome
            
            if form.quantidade:
                db_produto.quantidade = form.quantidade
            
            if form.valor:
                db_produto.valor = form.valor

            if form.data_validade:
                db_produto.data_validade = datetime.strptime( form.data_validade, '%d/%m/%Y' )

            session.add(db_produto)
            session.commit()
            return apresenta_produto(db_produto), 200
    
    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Produto de mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        return {"mesage": error_msg}, 400
    

@app.get('/produtos', tags=[gescom_tag],
         responses={"200": ListagemProdutosSchema, "404": ErrorSchema})
def get_produtos():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de produtos.
    """
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produtos = session.query(Produto).all()

    if not produtos:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
    else:
        # retorna a representação de produto
        return apresenta_produtos(produtos), 200


@app.get('/produto', tags=[gescom_tag],
         responses={"200": ProdutoViewSchema, "404": ErrorSchema})
def get_produto(query: ProdutoBuscaSchema):
    """Faz a busca por um Produto a partir do id do produto

    Retorna uma representação dos produtos e comentários associados.
    """
    produto_id = query.produto_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    produto = session.query(Produto).filter(Produto.id == produto_id).first()

    if not produto:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_produto(produto), 200


@app.delete('/produto', tags=[gescom_tag],
            responses={"200": ProdutoDelSchema, "404": ErrorSchema})
def del_produto(query: ProdutoBuscaSchema):
    """Deleta um Produto a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    produto_id = query.produto_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Produto).filter(Produto.id == produto_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Produto removido", "id": produto_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        return {"mesage": error_msg}, 404


"""
   Abaixo segue os metodos POST/GET/Delete da base Usuario.
"""

@app.post('/usuario', tags=[gescom_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_usuario(form: UsuarioSchema):
    """ Adiciona um novo Usuario à base de dados

    Retorna uma representação dos usuarios.
    """
    usuario = Usuario(
        nome = form.nome,
        email = form.email,
        senha = base64.b64encode( form.senha.encode() ) 
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionado usuario
        session.add(usuario)
        # efetivando o comando de adição de novo usuario na tabela.
        session.commit()
        return apresenta_usuario(usuario), 200
    
    except IntegrityError as e:
        # duplicidade no Email - IntegrityError
        error_msg = "Email já existe na base :/"
        return {"message": error_msg}, 409
    
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo usuario :/"
        return {"mesage": error_msg}, 400       


@app.post('/update_usuario', tags=[gescom_tag],
          responses={"200": UsuarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_usuario(form: UpdateUsuarioSchema ):
    """Edita um Usuario já salvo na base de dados

    Retorna uma representação do usuario.
    """

    id = form.id
    #senha   = base64.b64encode( form.senha.encode() )

    session = Session()
    
    try:
        query = session.query(Usuario).filter(Usuario.id == id)
        db_usuario = query.first()
        if not db_usuario:
            # se o usuario não foi encontrado
            error_msg = "Usuário não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.nome:
                db_usuario.nome = form.nome
            
            if form.email:
                db_usuario.email = form.email

            """
            if form.senha:
                db_usuario.senha = usuario.senha
            """

            session.add(db_usuario)
            session.commit()
            return apresenta_usuario(db_usuario), 200
    
    except IntegrityError as e:
        # como a duplicidade do email é a provável razão do IntegrityError
        error_msg = "Email com mesmo nome já salvo na base :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível alterar novo usuário :/"
        return {"mesage": error_msg}, 400


@app.get('/usuarios', tags=[gescom_tag],
         responses={"200": ListagemUsuariosSchema, "404": ErrorSchema})
def get_usuarios():
    """ Faz a busca por todos os Usuarios cadastrados

    Retorna uma representação da Listagem de usuarios.
    """         
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuarios = session.query(Usuario).all()

    if not usuarios:
        # se não ha usuarios cadastrados
        return {"usuarios": []}, 200         
    else:
         # retorna a representação dos usuarios
         return apresenta_usuarios(usuarios), 200      


@app.get('/usuario', tags=[gescom_tag],
         responses={"200": UsuarioDelSchema, "404": ErrorSchema})    
def get_usuario(query: UsuarioBuscaSchema):
    """ Faz a busca por um Usuario a partir do ID

    Retorna uma representação do Usuario.
    """         
    usuario_id = query.usuario_id
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        error_msg = "Usuario não encontrado na base :/"
        return {"message": error_msg}, 404
    else:
        return apresenta_usuario(usuario), 200


@app.delete('/usuario', tags=[gescom_tag],
            responses={"200": UsuarioDelSchema, "404": ErrorSchema})    
def del_usuario(query:UsuarioBuscaSchema):
    """ Deleta um usuario a partir do id informado
    
    Retorna uma mensagem de confirmação da remoção.
    """         
    usuario_id = query.usuario_id

    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Usuario).filter(Usuario.id == usuario_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"message": "Usuario removido", "id": usuario_id}
    else:
        # se o usuario não foi encontrado
        error_msg = "Usuário não encontrado na base :/"
        return {"message": error_msg}, 404


@app.post('/validaLogin', tags=[gescom_tag],
          responses={"200": UsuarioViewSchema, "404": ErrorSchema})
def valida_login(form: UsuarioValidaLoginSchema):
    """ 
        busca um usuario a partir do email e senha

    Retorna uma representação da Listagem de usuarios.
    """        
    usuario = Usuario(
        email   = form.email,
        senha   = form.senha
    )

    senha_s = base64.b64encode( form.senha.encode() )

    try:
        # criando conexão com a base
        session = Session()   
        # fazendo a busca
        query = session.query(Usuario).filter( Usuario.email == usuario.email, Usuario.senha == senha_s )  

        if query.count() == 0:
            error_msg = "Email não encontrado ou senha incorreta na base :/"
            return {"message": error_msg}, 404
        else:
            return apresenta_login(usuario), 200
        
    except Exception as e:
        error_msg = "Não foi possível encontrar o usuario: /"
        return {"mesage": error_msg}, 400       

"""
   Abaixo segue os metodos POST/GET/Delete/PUT da base Pessoa.
"""

@app.post('/pessoa', tags=[gescom_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pessoa(form: PessoaSchema):
    """Adiciona um nova Pessoa à base de dados

    Retorna uma representação das pessoas.
    """
    pessoa = Pessoa(
        cpf         = form.cpf,
        nome        = form.nome,
        cep         = form.cep,
        logradouro  = form.logradouro,
        complemento = form.complemento,
        numero      = form.numero,
        bairro      = form.bairro,
        cidade      = form.cidade,
        uf          = form.uf,
        ibge        = form.ibge    
    )    

    try:
        session = Session()
        session.add(pessoa)
        session.commit()
        return apresenta_pessoa(pessoa), 200

    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "CPF já existe na base de Dados :/"
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova pessoa :/"
        return {"mesage": error_msg}, 400


@app.put('/update_pessoa', tags=[gescom_tag],
          responses={"200": PessoaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_pessoa(form: UpdatePessoaSchema):
    """Edita uma Pessoa já salvo na base de dados

    Retorna uma representação da pessoa.
    """
    id_pessoa = form.id
    session = Session()
    
    try:
        query = session.query(Pessoa).filter(Pessoa.id == id_pessoa)
        db_pessoa = query.first()
        if not db_pessoa:
            # se a pessoa não foi encontrada
            error_msg = "Pessoa não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.cpf:
                db_pessoa.cpf = form.cpf

            if form.nome:
                db_pessoa.nome = form.nome
            
            if form.cep:
                db_pessoa.cep = form.cep
            
            if form.logradouro:
                db_pessoa.logradouro = form.logradouro

            if form.complemento:
                db_pessoa.complemento = form.complemento
            
            if form.numero:
                db_pessoa.numero = form.numero

            if form.bairro:
                db_pessoa.bairro = form.bairro

            if form.cidade:
                db_pessoa.cidade = form.cidade

            if form.uf:
                db_pessoa.uf = form.uf

            if form.ibge:
                db_pessoa.ibge = form.ibge

            session.add(db_pessoa)
            session.commit()
            return apresenta_pessoa(db_pessoa), 200
    
    except IntegrityError as e:
        # como a duplicidade do cpf é a provável razão do IntegrityError
        error_msg = "CPF já existe na base de Dados :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova pessoa :/"
        return {"mesage": error_msg}, 400


@app.get('/pessoas', tags=[gescom_tag],
         responses={"200": ListagemPessoasSchema, "404": ErrorSchema})
def get_pessoas():
    """Faz a busca por todos as Pessoas cadastradas

    Retorna uma representação da listagem de pessoas
    """
    session = Session()
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        # se não há pessoas cadastradas
        return {"pessoas": []}, 200
    else:
        # retorna a representação de pessoas
        return apresenta_pessoas(pessoas), 200


@app.get('/pessoa', tags=[gescom_tag],
         responses={"200": PessoaViewSchema, "404": ErrorSchema})
def get_pessoa(query: PessoaBuscaSchema):
    """Faz a busca por uma Pessoa a partir do id.

    Retorna uma representação da pessoa.
    """
    pessoa_id = query.pessoa_id
    session = Session()
    pessoa = session.query(Pessoa).filter(Pessoa.id == pessoa_id).first()

    if not pessoa:
        # se o pessoa não foi encontrada
        error_msg = "Pessoa não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_pessoa(pessoa), 200


@app.delete('/pessoa', tags=[gescom_tag],
            responses={"200": PessoaDelSchema, "404": ErrorSchema})
def del_pessoa(query: PessoaBuscaSchema):
    """Deleta uma Pessoa a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    pessoa_id = query.pessoa_id

    session = Session()
    count = session.query(Pessoa).filter(Pessoa.id == pessoa_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Pessoa removida", "id": pessoa_id}
    else:
        # se o pessoa não foi encontrada
        error_msg = "Pessoa não encontrada na base :/"
        return {"mesage": error_msg}, 404


"""
   Abaixo segue os metodos POST/GET/Delete/PUT da base Grupo.
"""

@app.post('/grupo', tags=[gescom_tag],
          responses={"200": GrupoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_grupo(form: GrupoSchema):
    """Adiciona um novo Grupo à base de dados

    Retorna uma representação de grupos.
    """
    grupo = Grupo(
        descricao   = form.descricao,
        margem      = form.margem
    )    

    try:
        session = Session()
        session.add(grupo)
        session.commit()
        return apresenta_grupo(grupo), 200

    except IntegrityError as e:
        # como a duplicidade da descricao é a provável razão do IntegrityError
        error_msg = "Descricao já existe na base de Dados :/"
        return {"mesage": error_msg }, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar um novo grupo :/"
        return {"mesage": error_msg}, 400


@app.put('/updateGrupo', tags=[gescom_tag],
          responses={"200": GrupoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_grupo(form: UpdateGrupoSchema):
    """Edita um Grupo já salvo na base de dados

    Retorna uma representação do grupo.
    """
    id_grupo = form.id
    session = Session()
    
    try:
        query = session.query(Grupo).filter(Grupo.id == id_grupo)
        db_grupo = query.first()
        if not db_grupo:
            # se o grupo não foi encontrado
            error_msg = "Grupo não encontrado na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.descricao:
                db_grupo.descricao = form.descricao

            if form.margem:
                db_grupo.margem = form.margem

            session.add(db_grupo)
            session.commit()
            return apresenta_grupo(db_grupo), 200
    
    except IntegrityError as e:
        # como a duplicidade da descricao é a provável razão do IntegrityError
        error_msg = "Descrição já existe na base de Dados :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar um novo grupo :/"
        return {"mesage": error_msg}, 400


@app.get('/grupos', tags=[gescom_tag],
         responses={"200": ListagemGruposSchema, "404": ErrorSchema})
def get_grupos():
    """Faz a busca por todos os Grupos cadastrados

    Retorna uma representação da listagem de grupos
    """
    session = Session()
    grupos  = session.query(Grupo).all()

    if not grupos:
        # se não há grupos cadastrado
        return {"grupos": []}, 200
    else:
        # retorna a representação de grupos
        return apresenta_grupos(grupos), 200


@app.get('/grupo', tags=[gescom_tag],
         responses={"200": GrupoViewSchema, "404": ErrorSchema})
def get_grupo(query: GrupoBuscaSchema):
    """Faz a busca por um Grupo a partir do id.

    Retorna uma representação da grupo.
    """
    grupo_id = query.grupo_id
    session = Session()
    grupo = session.query(Grupo).filter(Grupo.id == grupo_id).first()

    if not grupo:
        # se o grupo não foi encontrada
        error_msg = "Grupo não encontrado na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação de produto
        return apresenta_grupo(grupo), 200


@app.delete('/grupo', tags=[gescom_tag],
            responses={"200": GrupoDelSchema, "404": ErrorSchema})
def del_grupo(query: GrupoBuscaSchema):
    """Deleta um Grupo a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    grupo_id = query.grupo_id

    session = Session()
    count = session.query(Grupo).filter(Grupo.id == grupo_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Grupo removido", "id": grupo_id}
    else:
        # se o grupo não foi encontrado
        error_msg = "Grupo não encontrado na base :/"
        return {"mesage": error_msg}, 404


"""
   Abaixo segue os metodos POST/GET/Delete/PUT da base Marca.
"""

@app.post('/marca', tags=[gescom_tag],
          responses={"200": MarcaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_marca(form: MarcaSchema):

    """Adiciona uma nova Marca à base de dados

    Retorna uma representação de marcas.
    """
    marca = Marca(
        descricao   = form.descricao,
    )    

    try:
        session = Session()
        session.add(marca)
        session.commit()
        return apresenta_marca(marca), 200

    except IntegrityError as e:
        # como a duplicidade da descricao é a provável razão do IntegrityError
        error_msg = "Descricao já existe na base de Dados :/"
        return {"mesage": error_msg }, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar um novo grupo :/"
        return {"mesage": error_msg}, 400


@app.put('/updateMarca', tags=[gescom_tag],
          responses={"200": MarcaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_marca(form: UpdateMarcaSchema):
    """Edita uma Marca já salvo na base de dados

    Retorna uma representação de marca.
    """
    id_marca = form.id
    session = Session()
    
    try:
        query = session.query(Marca).filter(Marca.id == id_marca)
        db_marca = query.first()
        if not db_marca:
            # se a marca não foi encontrado
            error_msg = "Marca não encontrada na base :/"
            return {"mesage": error_msg}, 404
        else:
            if form.descricao:
                db_marca.descricao = form.descricao
            
            session.add(db_marca)
            session.commit()
            return apresenta_marca(db_marca), 200
    
    except IntegrityError as e:
        # como a duplicidade da descricao é a provável razão do IntegrityError
        error_msg = "Descrição já existe na base de Dados :/"
        return {"mesage": error_msg}, 409          
        
    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar um novo grupo :/"
        return {"mesage": error_msg}, 400


@app.get('/marcas', tags=[gescom_tag],
         responses={"200": ListagemMarcasSchema, "404": ErrorSchema})
def get_marcas():
    """Faz a busca por todos os marcas cadastradas

    Retorna uma representação da listagem de marcas
    """
    session  = Session()
    db_marca = session.query(Marca).all()

    if not db_marca:
        # se não há marcas cadastrada
        return {"marcas": []}, 200
    else:
        # retorna a representação de marcas
        return apresenta_marcas(db_marca), 200


@app.get('/marca', tags=[gescom_tag],
         responses={"200": MarcaViewSchema, "404": ErrorSchema})
def get_marca(query: MarcaBuscaSchema):
    """Faz a busca por uma marca a partir do id.

    Retorna uma representação da marca.
    """
    marca_id = query.marca_id
    session  = Session()
    db_marca = session.query(Marca).filter(Marca.id == marca_id).first()

    if not db_marca:
        # se o marca não foi encontrada
        error_msg = "Marca não encontrada na base :/"
        return {"mesage": error_msg}, 404
    else:
        # retorna a representação da marca
        return apresenta_marca(db_marca), 200


@app.delete('/marca', tags=[gescom_tag],
            responses={"200": MarcaDelSchema, "404": ErrorSchema})
def del_marca(query: MarcaBuscaSchema):
    """Deleta uma marca a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    marca_id = query.marca_id

    session = Session()
    count = session.query(Marca).filter(Marca.id == marca_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        return {"mesage": "Marca removido", "id": marca_id }
    else:
        # se a marca não foi encontrada
        error_msg = "Marca não encontrada na base :/"
        return {"mesage": error_msg}, 404
