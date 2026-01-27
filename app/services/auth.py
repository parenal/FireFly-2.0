import hashlib
from app.database_users import SessionUsers
from app.models.user import User


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username, password, name, surname):
    db = SessionUsers()
    try:
        if db.query(User).filter(User.username == username).first():
            return False, "El usuario ya existe"

        user = User(
            username=username,
            password_hash=hash_password(password),
            name=name,
            surname=surname
        )

        db.add(user)
        db.commit()
        return True, "Usuario creado"
    finally:
        db.close()


def authenticate_user(username, password):
    db = SessionUsers()
    try:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None

        if user.password_hash != hash_password(password):
            return None

        return user
    finally:
        db.close()