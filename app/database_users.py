import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Carpeta data/
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Base de datos de usuarios
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'users.db')}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
