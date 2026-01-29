from sqlalchemy.orm import Session
from app.database import UsersSessionLocal
from app.models.user import User
import hashlib
import logging
import tempfile
import os

# Setup a small file logger for auth debugging early so imports can log failures
_LOG_PATH = os.path.join(tempfile.gettempdir(), "firefly_auth.log")
_logger = logging.getLogger("firefly.auth")
if not _logger.handlers:
    fh = logging.FileHandler(_LOG_PATH, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    _logger.addHandler(fh)
    _logger.setLevel(logging.DEBUG)

# Prefer passlib CryptContext with Argon2/PBKDF2/Bcrypt if available
_HAS_PASSLIB = False
_CRYPT_CTX = None
try:
    _logger.debug("auth init: attempting to import passlib.context.CryptContext")
    from passlib.context import CryptContext

    try:
        _CRYPT_CTX = CryptContext(schemes=["argon2", "pbkdf2_sha256", "bcrypt"], deprecated="auto")
        _HAS_PASSLIB = True
        _logger.debug("auth init: CryptContext created successfully")
    except Exception as e:
        _HAS_PASSLIB = False
        _CRYPT_CTX = None
        _logger.exception("auth init: CryptContext construction failed: %s", e)
except Exception as e:
    _HAS_PASSLIB = False
    _CRYPT_CTX = None
    _logger.exception("auth init: import passlib failed: %s", e)

# Also log if argon2 low-level is available (used by some backends)
try:
    import argon2
    _logger.debug("auth init: argon2 available: %s", getattr(argon2, '__version__', 'unknown'))
except Exception:
    _logger.debug("auth init: argon2 not available")

# Log resolved capability flags after initialization
_logger.debug("auth init: _HAS_PASSLIB=%s _CRYPT_CTX_present=%s", _HAS_PASSLIB, bool(_CRYPT_CTX))

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
        _logger.debug("hash_password: using CryptContext.hash")
        return _CRYPT_CTX.hash(password)
    _logger.debug("hash_password: using legacy sha256 hash")
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


# Setup a small file logger for auth debugging (writes to temp dir so exe can write)
_LOG_PATH = os.path.join(tempfile.gettempdir(), "firefly_auth.log")
_logger = logging.getLogger("firefly.auth")
if not _logger.handlers:
    fh = logging.FileHandler(_LOG_PATH, encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    _logger.addHandler(fh)
    _logger.setLevel(logging.DEBUG)




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
            _logger.debug("authenticate_user: user not found for %s", username_norm)
            return None

        # Use passlib CryptContext verify (auto-detects scheme) when available
        if _HAS_PASSLIB and _CRYPT_CTX is not None:
            try:
                _logger.debug("authenticate_user: trying CryptContext.verify for user %s", username_norm)
                if _CRYPT_CTX.verify(password, user.password_hash):
                    _logger.debug("authenticate_user: CryptContext.verify succeeded for %s", username_norm)
                    return user
            except Exception:
                import traceback
                _logger.exception("authenticate_user: CryptContext.verify raised exception for %s", username_norm)
                # verification failed or hash malformed: fall back to legacy
                pass

        # Legacy check (sha256 hex) as fallback
        try:
            _logger.debug("authenticate_user: trying legacy sha256 check for %s", username_norm)
            if user.password_hash == hashlib.sha256(password.encode("utf-8")).hexdigest():
                _logger.debug("authenticate_user: legacy sha256 check succeeded for %s", username_norm)
                return user
        except Exception:
            _logger.exception("authenticate_user: legacy sha256 check exception for %s", username_norm)
            pass

        _logger.debug("authenticate_user: authentication failed for %s", username_norm)
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
