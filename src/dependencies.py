from sqlalchemy.orm import sessionmaker
from models import db

def pegar_sessao(): #Cria sessao no banco e retorna a sessao como resposta
    try:
        Session = sessionmaker(bind=db) # criando conexao com o db
        session = Session() # abrindo uma instancia dessa conexao
        yield session # nao encerra a funcao. retorna, continua e volta aqui
    finally:
        session.close()