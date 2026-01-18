from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao
from main import bcrypt_context
from sqlalchemy.orm import Session
from schemas import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get('/')
async def home():
    """
    Essa é a rota padrão de autenticação do nosso sistema.
    """
    return {"msg": "Acessou a rota de autenticação", "autenticado": True}


@auth_router.post('/criar_conta')
async def criar_conta(
    usuario_schema: UsuarioSchema, 
    session: Session = Depends(pegar_sessao)
): # Sessao nao é um parametro do usuario. Depends (fastAPI) puxa a funcao
    
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() # Verifica se esse email ja existe
    if usuario:
        raise HTTPException(status_code=400, detail="Já existe um usuário com esse email!")
    
    # Se nao existir
    senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
    session.add(novo_usuario)
    session.commit()
    return { "msg": f"Usuário cadastrado com sucesso! {usuario_schema.email}"}