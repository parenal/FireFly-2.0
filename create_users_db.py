from app.database import users_engine
from app.models.user import User
from app.database import Base

Base.metadata.create_all(bind=users_engine)

print("Base de datos de usuarios creada correctamente")
