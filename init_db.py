from app.database import engine
from app.models import Base

Base.metadata.create_all(engine)
print("Base de datos creada correctamente")