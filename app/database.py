from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# ===== BASE TRANSACCIONES =====
DATABASE_URL = "sqlite:///data/finance.db"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ===== BASE USUARIOS =====
USERS_DATABASE_URL = "sqlite:///data/users.db"

users_engine = create_engine(USERS_DATABASE_URL, echo=False)
UsersSessionLocal = sessionmaker(bind=users_engine)