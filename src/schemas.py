# Pydantic força a tipagem de dados
from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional #dados opcionais

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True #Interpretado como uma classe, e nao um dict