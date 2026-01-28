from sqlalchemy import Column, Integer, String
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    username_hash = Column(String, unique=True, nullable=False)
    # name and surname will be stored encrypted (Fernet -> base64 string)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)