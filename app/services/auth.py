from sqlalchemy.orm import Session
from app.database import UsersSessionLocal
from app.models.user import User
import hashlib

# Prefer passlib CryptContext with Argon2/PBKDF2/Bcrypt if available
try:
    from passlib.context import CryptContext
    _HAS_PASSLIB = True
    _CRYPT_CTX = CryptContext(schemes=["argon2", "pbkdf2_sha256", "bcrypt"], deprecated="auto")
except Exception:
    _HAS_PASSLIB = False
    _CRYPT_CTX = None

# encryption helpers for user fields
try:
    from app.utils.crypto import encrypt_text, decrypt_text
    _HAS_CRYPTO = True
except Exception:
    _HAS_CRYPTO = False


# =========================
# UTILIDAD: HASH PASSWORD
# =========================
def hash_password(password: str) -> str:
    if _HAS_PASSLIB and _CRYPT_CTX is not None:
        return _CRYPT_CTX.hash(password)
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# =========================
# REGISTRAR USUARIO
# =========================
def create_user(username: str, name: str, surname: str, password: str) -> bool:
    db: Session = UsersSessionLocal()
    try:
        # comprobar si el usuario ya existe
        username_norm = username.strip().lower()
        username_hash = hashlib.sha256(username_norm.encode("utf-8")).hexdigest()
        existing = db.query(User).filter(User.username_hash == username_hash).first()
        if existing:
            return False

        enc_name = encrypt_text(name) if _HAS_CRYPTO else name
        enc_surname = encrypt_text(surname) if _HAS_CRYPTO else surname

        user = User(
            username=username,
            username_hash=username_hash,
            name=enc_name,
            surname=enc_surname,
            password_hash=hash_password(password)
        )

        db.add(user)
        db.commit()
        return True
    finally:
        db.close()


# =========================
# AUTENTICAR USUARIO
# =========================
def authenticate_user(username: str, password: str):
    db: Session = UsersSessionLocal()
    try:
        username_norm = username.strip().lower()
        username_hash = hashlib.sha256(username_norm.encode("utf-8")).hexdigest()

        user = db.query(User).filter(User.username_hash == username_hash).first()
        if not user:
            return None

        # Use passlib CryptContext verify (auto-detects scheme) when available
        if _HAS_PASSLIB and _CRYPT_CTX is not None:
            try:
                if _CRYPT_CTX.verify(password, user.password_hash):
                    return user
            except Exception:
                # verification failed or hash malformed: fall back to legacy
                pass

        # Legacy check (sha256 hex) as fallback
        try:
            if user.password_hash == hashlib.sha256(password.encode("utf-8")).hexdigest():
                return user
        except Exception:
            pass

        return None
    finally:
        db.close()


def get_user_by_username(username: str):
    db: Session = UsersSessionLocal()
    try:
        username_norm = username.strip().lower()
        username_hash = hashlib.sha256(username_norm.encode("utf-8")).hexdigest()
        return db.query(User).filter(User.username_hash == username_hash).first()
    finally:
        db.close()


def change_password(user_id: int, current_password: str, new_password: str) -> bool:
    """Cambia la contraseña si `current_password` es correcta. Devuelve True si cambió."""
    db: Session = UsersSessionLocal()
    try:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # verify current password using CryptContext (auto-detect) then fallback to legacy sha256
        verified = False
        if _HAS_PASSLIB and _CRYPT_CTX is not None:
            try:
                verified = _CRYPT_CTX.verify(current_password, user.password_hash)
            except Exception:
                verified = False

        if not verified:
            try:
                if user.password_hash == hashlib.sha256(current_password.encode("utf-8")).hexdigest():
                    verified = True
            except Exception:
                verified = False

        if not verified:
            return False

        # set new password hash using CryptContext if available (accepts long passwords)
        if _HAS_PASSLIB and _CRYPT_CTX is not None:
            try:
                new_hash = _CRYPT_CTX.hash(new_password)
            except ValueError as e:
                # map potential backend errors regarding length to sentinel
                msg = str(e).lower()
                if "72" in msg or "longer than 72" in msg or "72 bytes" in msg:
                    raise ValueError("password_too_long")
                raise
        else:
            new_hash = hashlib.sha256(new_password.encode("utf-8")).hexdigest()

        user.password_hash = new_hash
        db.commit()
        return True
    finally:
        db.close()
