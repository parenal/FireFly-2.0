import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Determine base directory for the bundled 'data' folder.
# When running frozen by PyInstaller, use sys._MEIPASS; otherwise use project root.
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
	_base_dir = sys._MEIPASS
else:
	_base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

DATA_DIR = os.path.join(_base_dir, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def _sqlite_url(path: str) -> str:
	p = os.path.abspath(path).replace("\\", "/")
	return f"sqlite:///{p}"

# ===== BASE TRANSACCIONES =====
DATABASE_URL = _sqlite_url(os.path.join(DATA_DIR, "finance.db"))
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# ===== BASE USUARIOS =====
USERS_DATABASE_URL = _sqlite_url(os.path.join(DATA_DIR, "users.db"))
users_engine = create_engine(USERS_DATABASE_URL, echo=False)
UsersSessionLocal = sessionmaker(bind=users_engine)