from sqlalchemy import Column, Integer, String
from .conexion import Base

class User(Base):
    __tablename__ = "testigos"
    id_testigo = Column(Integer, primary_key=True, index=True)
    cod_departamento = Column(String(20))
    cod_municipio = Column(String(20))
    zona = Column(String(20))
    cod_puesto = Column(String(20))
    nom_departamento = Column(String(20))
    nom_municipio = Column(String(100))
    nom_puesto = Column(String(100))
    mesa = Column(String(20))
    organizacion = Column(String(20))
    tipo_testigo = Column(String(20))
    num_documento = Column(String(20))
    nombre = Column(String(20))
    segundo_nombre =Column(String(20))
    apellido = Column(String(20))
    segundo_apellido = Column(String(20))
    celular = Column(String(20))
    correo = Column(String(20))
    tipo_credencial  = Column(String(20))
    resolucion = Column(String(20))
    comision = Column(String(20))
