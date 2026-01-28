from cryptography.fernet import Fernet
import os


def _key_path():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    return os.path.join(root, "data", "secret.key")


def ensure_key():
    path = _key_path()
    dirp = os.path.dirname(path)
    os.makedirs(dirp, exist_ok=True)
    if not os.path.exists(path):
        key = Fernet.generate_key()
        with open(path, "wb") as f:
            f.write(key)
        return key
    with open(path, "rb") as f:
        return f.read()


def get_fernet():
    key = ensure_key()
    return Fernet(key)


def encrypt_text(plain: str) -> str:
    if plain is None:
        return ""
    f = get_fernet()
    token = f.encrypt(plain.encode("utf-8"))
    return token.decode("utf-8")


def decrypt_text(token: str) -> str:
    if not token:
        return ""
    f = get_fernet()
    try:
        return f.decrypt(token.encode("utf-8")).decode("utf-8")
    except Exception:
        return ""
