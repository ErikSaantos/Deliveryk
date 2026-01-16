from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import declarative_base
from enum import Enum

# Cria a conexão com o banco
db = create_engine("sqlite:///database/banco.db")

# Cria a base do banco
Base = declarative_base()


# Cria as classes/tabelas do banco

class StatusPedido(Enum):
    """"
    Regra no campo Status usando Enum -> 'PENDENTE', 'CANCELADO', 'FINALIZADO'
    """
    PENDENTE = 'PENDENTE'
    CANCELADO = 'CANCELADO'
    FINALIZADO = 'FINALIZADO'


# Usuario
class Usuario(Base):
    __tablename__ = "usuarios" #Define nome da tabela manualmente. SQLAlchemy adiciona um 's' no final por padrao

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String, nullable=False)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin


# Pedido
class Pedido(Base):
    __tablename__ = "pedidos"
    
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    status = Column(SQLEnum(StatusPedido, name="status_pedido_enum"), default=StatusPedido.PENDENTE) # pendente, cancelado, finalizado
    preco = Column("preco", Float)
    # itens = 

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.status = status
        self.preco = preco


# ItensPedidos
class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    tipo_borda = Column("tipo_borda", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id"))

    def __init__(self, quantidade, sabor, tamanho, tipo_borda, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.tipo_borda = tipo_borda
        self.preco_unitario = preco_unitario
        self.pedido = pedido
