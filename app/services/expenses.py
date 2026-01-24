from app.database import SessionLocal
from app.models.transaction import Transaction


# =========================
# CREAR TRANSACCIÓN
# =========================
def add_transaction(t_type, amount, category, description=None, date=None):
    db = SessionLocal()
    try:
        tx = Transaction(
            type=t_type,
            amount=amount,
            category=category.strip().capitalize(),
            description=description,
            date=date
        )
        db.add(tx)
        db.commit()
    finally:
        db.close()


# =========================
# LISTAR TRANSACCIONES
# =========================
def list_transactions(limit=100):
    db = SessionLocal()
    try:
        return (
            db.query(Transaction)
            .order_by(Transaction.date.desc(), Transaction.id.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


# =========================
# OBTENER UNA TRANSACCIÓN
# =========================
def get_transaction_by_id(transaction_id):
    db = SessionLocal()
    try:
        return db.query(Transaction).filter(Transaction.id == transaction_id).first()
    finally:
        db.close()


# =========================
# ACTUALIZAR TRANSACCIÓN
# =========================
def update_transaction(
    transaction_id,
    t_type,
    amount,
    category,
    description,
    date
):
    db = SessionLocal()
    try:
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx:
            return

        tx.type = t_type
        tx.amount = amount
        tx.category = category.strip().capitalize()
        tx.description = description
        tx.date = date

        db.commit()
    finally:
        db.close()


# =========================
# ELIMINAR TRANSACCIÓN
# =========================
def delete_transaction(transaction_id):
    db = SessionLocal()
    try:
        tx = db.query(Transaction).filter(Transaction.id == transaction_id).first()
        if not tx:
            return

        db.delete(tx)
        db.commit()
    finally:
        db.close()