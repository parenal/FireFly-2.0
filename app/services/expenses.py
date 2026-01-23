from app.database import SessionLocal
from app.models import Transaction


# =========================
# Crear transacción
# =========================
def add_transaction(t_type, amount, category, description=None, date=None):
    session = SessionLocal()

    normalized_category = category.strip().lower().capitalize() if category else None

    tx = Transaction(
        type=t_type.lower(),   # "income" o "expense"
        amount=amount,
        category=normalized_category,
        description=description,
        date=date
    )

    session.add(tx)
    session.commit()
    session.close()


# =========================
# Listar transacciones
# =========================
def list_transactions(limit=100):
    session = SessionLocal()

    txs = (
        session
        .query(Transaction)
        .order_by(Transaction.date.desc(), Transaction.id.desc())
        .limit(limit)
        .all()
    )

    session.close()
    return txs


# =========================
# Eliminar transacción
# =========================
def delete_transaction(tx_id):
    session = SessionLocal()

    tx = session.get(Transaction, tx_id)
    if tx:
        session.delete(tx)
        session.commit()

    session.close()


# =========================
# Actualizar transacción
# =========================
def update_transaction(
    tx_id,
    t_type,
    amount,
    category,
    description=None,
    date=None
):
    session = SessionLocal()

    tx = session.get(Transaction, tx_id)
    if not tx:
        session.close()
        return

    tx.type = t_type.lower()
    tx.amount = amount
    tx.category = category.strip().lower().capitalize() if category else None
    tx.description = description
    tx.date = date

    session.commit()
    session.close()


# =========================
# Categorías existentes
# =========================
def get_existing_categories(t_type):
    session = SessionLocal()

    rows = (
        session
        .query(Transaction.category)
        .filter(Transaction.type == t_type.lower())
        .distinct()
        .all()
    )

    session.close()

    return sorted(
        [row[0] for row in rows if row[0]]
    )
