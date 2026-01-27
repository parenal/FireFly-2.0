from app.database import UsersSessionLocal
from app.models.user import User

import hashlib


# =========================
# UTILIDADES
# =========================
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# =========================
# REGISTRO
# =========================
def register_user(username, name, surname, password):
    db = UsersSessionLocal()
    try:
        existing = db.query(User).filter(User.username == username).first()
        if existing:
            return False, "El usuario ya existe"

        user = User(
            username=username,
            name=name,
            surname=surname,
            password_hash=hash_password(password)
        )

        db.add(user)
        db.commit()
        return True, None
    finally:
        db.close()


# =========================
# LOGIN
# =========================
def authenticate_user(username, password):
    db = UsersSessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        if user.password_hash != hash_password(password):
            return None

        return user
    finally:
        db.close()