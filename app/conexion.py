import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Captura DATABASE_URL o MYSQL_URL por si Railway usa el nombre por defecto
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")

# Si por alguna razón sigue siendo None, asignamos la URL privada directa
if not DATABASE_URL:
    DATABASE_URL = "mysql://root:qQzoaRbhRGmOGKYaBAPxrrfZpeQusGXN@mysql.railway.internal:3306/testigos-electorales"

# Convertir el driver para SQLAlchemy
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace("mysql://", "mysql+pymysql://", 1)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Corrección de tipografía: SessionLocal (sin la 'a' extra)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()