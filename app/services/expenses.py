from app.database import SessionLocal
from app.models import Transaction

def add_transaction(t_type, amount, category, description=None, date=None):
    session = SessionLocal()

    # Normalizar categoría: primera letra mayúscula
    normalized_category = category.strip().lower().capitalize()

    tx = Transaction(
        type=t_type.lower(),   # también normalizamos el tipo
        amount=amount,
        category=normalized_category,
        description=description,
        date=date
    )

    session.add(tx)
    session.commit()
    session.close()


def list_transactions(limit=20):
    session = SessionLocal()
    txs = (
        session
        .query(Transaction)
        .order_by(Transaction.date.desc())
        .limit(limit)
        .all()
    )
    session.close()
    return txs
