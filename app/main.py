from fastapi import FastAPI, Depends, HTTPException
from typing import List
from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

from fastapi.middleware.cors import CORSMiddleware 
from starlette.responses import RedirectResponse

from . import models, schemas
from .conexion import SessionLocal, engine

from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Permite peticiones desde Angular
    allow_credentials=True,
    allow_methods=["*"],              # Permite todos los métodos (POST, GET, PUT, DELETE, etc.)
    allow_headers=["*"],              # Permite todos los headers
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

@app.get("/testigos/{num_documento}", response_model=schemas.User)
def get_testigo_by_documento(num_documento: str, db: Session = Depends(get_db)):
    # Buscamos en la tabla por la columna num_documento
    testigo = db.query(models.User).filter(models.User.num_documento == num_documento).first()
    
    if not testigo:
        raise HTTPException(status_code=404, detail="Testigo no encontrado en la base de datos")
        
    return testigo

@app.get("/testigos/", response_model=List[schemas.User])
def show_users(db:Session = Depends(get_db)):
    testigos =db.query(models.User).all()
    return testigos

@app.post("/testigos/", response_model=schemas.User)
def create_users(entrada:schemas.User,db:Session = Depends(get_db)):
    usuario = models.User(
        cod_departamento = entrada.cod_departamento, 
        cod_municipio = entrada.cod_municipio, 
        zona = entrada.zona, 
        cod_puesto = entrada.cod_puesto, 
        nom_departamento = entrada.nom_departamento, 
        nom_municipio=entrada.nom_municipio, 
        nom_puesto=entrada.nom_puesto, 
        mesa=entrada.mesa, 
        organizacion=entrada.organizacion, 
        tipo_testigo=entrada.tipo_testigo, 
        num_documento=entrada.num_documento, 
        nombre = entrada.nombre, 
        segundo_nombre= entrada.segundo_nombre, 
        apellido = entrada.apellido, 
        segundo_apellido = entrada.segundo_apellido, 
        celular = entrada.celular, 
        correo = entrada.correo, 
        tipo_credencial = entrada.tipo_credencial, 
        resolucion = entrada.resolucion,
        comision = entrada.comision )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

@app.put("/testigos/{id_testigo}", response_model=schemas.User)
def create_users(id_testigo:int, entrada:schemas.User,db:Session = Depends(get_db)):
    usuario = db.query(models.User).filter_by(id=id_testigo).first()
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@app.post("/testigos/bulk", status_code=201)
def create_users_bulk(entrada_lista: List[schemas.User], db: Session = Depends(get_db)):
    nuevos_usuarios = []

    for entrada in entrada_lista:
        usuario = models.User(
            cod_departamento=entrada.cod_departamento,
            cod_municipio=entrada.cod_municipio,
            zona=entrada.zona,
            cod_puesto=entrada.cod_puesto,
            nom_departamento=entrada.nom_departamento,
            nom_municipio=entrada.nom_municipio,
            nom_puesto=entrada.nom_puesto,
            mesa=entrada.mesa,
            organizacion=entrada.organizacion,
            tipo_testigo=entrada.tipo_testigo,
            num_documento=entrada.num_documento,
            nombre=entrada.nombre,
            segundo_nombre=entrada.segundo_nombre,
            apellido=entrada.apellido,
            segundo_apellido=entrada.segundo_apellido,
            celular=entrada.celular,
            correo=entrada.correo,
            tipo_credencial = entrada.tipo_credencial,
            resolucion=entrada.resolucion,
            comision = entrada.comision 

        )
        nuevos_usuarios.append(usuario)

    try:
        # Añade todos los registros a la sesión en una sola transacción
        db.add_all(nuevos_usuarios)
        db.commit()
        return {"status": "success", "inserted": len(nuevos_usuarios)}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}