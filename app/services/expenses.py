from app.database import SessionLocal
from app.models import Transaction

def add_transaction(t_type, amount, category, description=None, date=None):
    session = SessionLocal()
    tx = Transaction(
        type=t_type,
        amount=amount,
        category=category,
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
