import os
import sys
from sqlalchemy import create_engine, MetaData, Table, select

# add project root to path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root not in sys.path:
    sys.path.insert(0, root)

from app.database import UsersSessionLocal, users_engine, Base
from app.models.user import User
from sqlalchemy import inspect, text

try:
    from app.utils.crypto import encrypt_text
    _HAS_CRYPTO = True
except Exception:
    _HAS_CRYPTO = False

import hashlib

BACKUP_PATH = os.path.join(root, "data", "users.db.bak")
NEW_DB = os.path.join(root, "data", "users.db")


def main():
    if not os.path.exists(BACKUP_PATH):
        print(f"Backup DB not found at {BACKUP_PATH}. Aborting.")
        return

    print("Opening backup DB:", BACKUP_PATH)
    backup_engine = create_engine(f"sqlite:///{BACKUP_PATH}", echo=False)
    meta = MetaData()
    meta.reflect(bind=backup_engine)

    if "users" not in meta.tables:
        print("No 'users' table found in backup DB. Aborting.")
        return

    users_table = meta.tables["users"]
    conn = backup_engine.connect()
    rows = conn.execute(select(users_table)).mappings().all()
    print(f"Found {len(rows)} users in backup.")

    # Ensure target tables exist (create missing tables)
    try:
        Base.metadata.create_all(bind=users_engine)
    except Exception as e:
        print("Warning: could not create tables:", e)

    # If the users table exists but is missing the new column, add it (SQLite can't alter schema via create_all)
    try:
        inspector = inspect(users_engine)
        cols = [c['name'] for c in inspector.get_columns('users')]
        if 'username_hash' not in cols:
            print('Adding username_hash column to users table')
            with users_engine.connect() as conn:
                conn.execute(text('ALTER TABLE users ADD COLUMN username_hash TEXT'))
                conn.commit()
    except Exception as e:
        print('Warning while ensuring users table schema:', e)

    db = UsersSessionLocal()
    imported = 0
    updated = 0
    skipped = 0
    for r in rows:
        username = r.get("username") or r.get("user")
        if not username:
            skipped += 1
            continue
        username_norm = username.strip().lower()
        username_hash = hashlib.sha256(username_norm.encode("utf-8")).hexdigest()
        # try find existing by username_hash
        exists_hash = db.query(User).filter(User.username_hash == username_hash).first()
        if exists_hash:
            skipped += 1
            continue

        # try find existing by username (older DB may have plain username)
        exists_user = db.query(User).filter(User.username == username).first()

        name = r.get("name") or ""
        surname = r.get("surname") or ""
        password_hash = r.get("password_hash") or r.get("password") or ""

        if _HAS_CRYPTO:
            enc_name = encrypt_text(name)
            enc_surname = encrypt_text(surname)
        else:
            enc_name = name
            enc_surname = surname

        if exists_user:
            # update existing row: set username_hash and encrypt fields if not set
            if not getattr(exists_user, "username_hash", None):
                exists_user.username_hash = username_hash
            try:
                if _HAS_CRYPTO:
                    exists_user.name = enc_name
                    exists_user.surname = enc_surname
            except Exception:
                pass
            if not getattr(exists_user, "password_hash", None) and password_hash:
                exists_user.password_hash = password_hash

            db.add(exists_user)
            updated += 1
        else:
            user = User(
                username=username,
                username_hash=username_hash,
                name=enc_name,
                surname=enc_surname,
                password_hash=password_hash
            )
            db.add(user)
            imported += 1

        # commit per-row to avoid autoflush conflicts
        try:
            db.commit()
        except Exception:
            db.rollback()

    db.commit()
    db.close()
    conn.close()

    print(f"Imported: {imported}, Skipped: {skipped}")
    print("Migration complete.")


if __name__ == "__main__":
    main()
