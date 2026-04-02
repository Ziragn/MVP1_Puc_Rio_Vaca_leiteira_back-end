from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from datetime import date

from sqlalchemy.exc import IntegrityError

from model import Session, Vaca, RegistroProducao
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
vaca_tag = Tag(name="Vaca", description="Adição, visualização e remoção de vacas à base")
registro_tag = Tag(
    name="Registro de Produção",
    description="Cadastro e consulta de produção leiteira por data"
)



@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/vaca', tags=[vaca_tag],
          responses={"200": VacaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_vaca(form: VacaSchema):
    """Adiciona uma nova Vaca à base de dados

    Retorna uma representação das vacas
    """
    vaca = Vaca(
        nome=form.nome,
        raca=form.raca
        )
    logger.debug(f"Adicionando vaca de nome: '{vaca.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(vaca)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado vaca de nome: '{vaca.nome}'")
        return {
    "nome": vaca.nome,
    "raca": vaca.raca
}, 200

    except IntegrityError as e:
        session.rollback()
        error_msg = "Produto de mesmo nome já salvo na base :/"
        logger.warning(f"IntegrityError ao adicionar vaca '{vaca.nome}': {repr(e)}")
        return {"message": error_msg}, 409

    except Exception as e:
        session.rollback()
        logger.error(f"Erro real ao adicionar vaca '{vaca.nome}': {repr(e)}")
        return {"message": str(e)}, 400


@app.get('/vacas', tags=[vaca_tag],
         responses={"200": ListagemVacasSchema, "404": ErrorSchema})
def get_vacas():
    """Faz a busca por todas as vacas cadastradas

    Retorna uma representação da listagem de vacas.
    """
    logger.debug(f"Coletando vacas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vacas = session.query(Vaca).all()

    if not vacas:
        # se não há vacas cadastrados
        return {"vacas": []}, 200
    else:
        logger.debug(f"%d vacas encontradas" % len(vacas))
        # retorna a representação de vaca
        print(vacas)
        return apresenta_vacas(vacas), 200


@app.get('/vaca', tags=[vaca_tag],
         responses={"200": VacaViewSchema, "404": ErrorSchema})
def get_produto(query: VacaBuscaSchema):
    """Faz a busca por uma vaca a partir do id do vaca

    Retorna uma representação das vacas
    """
    vaca_nome = query.nome
    logger.debug(f"Coletando dados sobre produto #{vaca_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    vaca = session.query(Vaca).filter(Vaca.nome == vaca_nome).first()

    if not vaca:
        # se a vaca não foi encontrado
        error_msg = "Vaca não encontrada na base :/"
        logger.warning(f"Erro ao buscar vaca '{vaca_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Vaca econtrada: '{vaca.nome}'")
        # retorna a representação da vaca
        return apresenta_vaca(vaca), 200


@app.delete('/vaca', tags=[vaca_tag],
            responses={"200": VacaDelSchema, "404": ErrorSchema})
def del_produto(query: VacaBuscaSchema):
    """Deleta uma vaca a partir do nome da vaca informada

    Retorna uma mensagem de confirmação da remoção.
    """
    vaca_nome = unquote(unquote(query.nome))
    print(vaca_nome)
    logger.debug(f"Deletando dados sobre a vaca #{vaca_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Vaca).filter(Vaca.nome == vaca_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada a vaca #{vaca_nome}")
        return {"mesage": "Vaca removido", "id": vaca_nome}
    else:
        # se a vaca não foi encontrada
        error_msg = "Vaca não encontrada na base :/"
        logger.warning(f"Erro ao deletar a vaca #'{vaca_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    
@app.post(
    '/registro_producao',
    tags=[registro_tag],
    responses={"200": RegistroViewSchema, "404": ErrorSchema, "400": ErrorSchema}
)
def add_registro_producao(form: RegistroProducaoSchema):
    """
    Adiciona um novo registro de produção para uma vaca.
    """
    session = Session()

    try:
        vaca = session.query(Vaca).filter(Vaca.nome == form.nome_vaca).first()

        if not vaca:
            return {"message": "Vaca não encontrada na base :/"}, 404

        if form.data_registro > date.today():
            return {"message": "A data do registro não pode ser futura."}, 400

        registro = RegistroProducao(
            data_registro=form.data_registro,
            litros=form.litros,
            vaca_id=vaca.id
        )

        session.add(registro)
        session.commit()

        return apresenta_registro(registro, vaca.nome), 200

    except Exception as e:
        session.rollback()
        return {"message": str(e)}, 400

@app.get(
    '/registro_producao',
    tags=[registro_tag],
    responses={"200": ListagemRegistrosSchema, "404": ErrorSchema}
)
def get_registros_producao(query: RegistroBuscaSchema):
    """
    Lista os registros de produção de uma vaca pelo nome.
    """
    session = Session()

    vaca = session.query(Vaca).filter(Vaca.nome == query.nome_vaca).first()

    if not vaca:
        return {"message": "Vaca não encontrada na base :/"}, 404

    registros = session.query(RegistroProducao).filter(
        RegistroProducao.vaca_id == vaca.id
    ).all()

    return apresenta_registros(registros, vaca.nome), 200

@app.get(
    '/vaca/media_producao',
    tags=[registro_tag],
    responses={"200": ErrorSchema, "404": ErrorSchema}
)
def get_media_producao(query: RegistroBuscaSchema):
    """
    Calcula a média de produção registrada de uma vaca.
    """
    session = Session()

    vaca = session.query(Vaca).filter(Vaca.nome == query.nome_vaca).first()

    if not vaca:
        return {"message": "Vaca não encontrada na base :/"}, 404

    registros = session.query(RegistroProducao).filter(
        RegistroProducao.vaca_id == vaca.id
    ).all()

    if not registros:
        return {"message": "Essa vaca não possui registros de produção."}, 404

    media = sum(r.litros for r in registros) / len(registros)

    return {
        "nome_vaca": vaca.nome,
        "media_producao": round(media, 2),
        "quantidade_registros": len(registros)
    }, 200





