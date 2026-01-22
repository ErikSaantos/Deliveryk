from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc)+ duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM) # (dicionario de informacoes, chave secreta como referencia, algoritmo de codificação)
    return jwt_codificado


def autenticar_usuario(email, senha, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): # recebe senha e hash, e compara se nao são a mesma coisa
        return False
    return usuario
    

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


# Login via Token -> JWT Bearer
@auth_router.post("/login")
async def login(
    login_schema: LoginSchema, 
    session: Session = Depends(pegar_sessao)
):
    """
    Rota de login do usuário onde retorna um token de 30 minutos.
    Usa a função de autenticar usuário (procura no banco). Se não achar devolve um code=400, mas se achar cria e devolve um Token Bearer de 30 minutos
    """
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas")
    access_token = criar_token(usuario.id) # 30min, usa pra fazer requisições
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7)) # 7 dias, usa pra criar outro access token
    return {
        "access-token": access_token,
        "refresh-token": refresh_token,
        "token-type": "Bearer"
    }
    #quando usuario faz requisicao, tem que passar o token pelos headers ˆˆˆ
    #headers = {"Access-Token": "Bearer-Token"}


@auth_router.get('/refresh')
async def use_refresh_token(
    usuario: Usuario = Depends(verificar_token) #Envia o token e volta um usuário
):
    """
    Verifica o token e gera um novo
    """
    access_token = criar_token(usuario.id)
    return {
        "access-token": access_token,
        "token-type": "Bearer"
    }