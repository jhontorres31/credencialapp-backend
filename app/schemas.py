from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    
    id_testigo: Optional[int] = None
    
    # Campos estrictamente obligatorios (No pueden venir vacíos)
    cod_departamento: str
    cod_municipio: str
    nom_departamento: str
    nom_municipio: str
    organizacion: str
    tipo_testigo: str
    num_documento: str
    nombre: str
    apellido: str
    tipo_credencial: str
    resolucion: str

    
    # Campos Opcionales (Si en el Excel vienen en blanco, no romperán la petición)

    segundo_nombre: Optional[str] = ""
    segundo_apellido: Optional[str] = ""
    cod_puesto: Optional [str] = ""
    zona: Optional [str] = ""
    nom_puesto: Optional [str] = ""
    mesa: Optional [str] = ""
    comision: Optional [str] = ""
    celular: Optional[str] = ""
    correo: Optional[str] = ""

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):

    nombre: str
    

    class Config:
        orm_mode = True