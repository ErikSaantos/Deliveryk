from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session, query
from models import db, Usuario
from jose import JWTError, jwt
from main import SECRET_KEY, ALGORITHM, oauth2_schema # DEPENDENCIES NAO IMPORTA MAIN !!! core/config.py

def pegar_sessao(): #Cria sessao no banco e retorna a sessao como resposta
    try:
        Session = sessionmaker(bind=db) # criando conexao com o db
        session = Session() # abrindo uma instancia dessa conexao
        yield session # nao encerra a funcao. retorna, continua e volta aqui
    finally:
        session.close()


def verificar_token( # Dependência pois se usará várias vezes
    token: str = Depends(oauth2_schema), # Recebe via headers
    session: Session = Depends(pegar_sessao)
):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub")) #ou dic_info["sub"] -> devolve erro se nao achar
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token.")

    # verifica se o token é valido
    # extrai o ID do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso Inválido.")
    return usuario # Retorna o usuário dono do token