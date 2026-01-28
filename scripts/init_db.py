import os
import sys

# Asegura que el directorio raíz del proyecto está en sys.path cuando
# se ejecuta este script directamente (python scripts/init_db.py)
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from app.database import engine, users_engine, Base
from app.models.user import User
from app.models.transaction import Transaction

# Crea las tablas necesarias en ambas bases de datos (si no existen)
if __name__ == "__main__":
    # Crear las tablas en la base de transacciones
    Base.metadata.create_all(bind=engine)

    # Crear las tablas en la base de usuarios (mismas clases, distinto engine)
    Base.metadata.create_all(bind=users_engine)

    print("Tablas creadas/actualizadas en data/finance.db y data/users.db")
