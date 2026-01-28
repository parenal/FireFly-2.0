from sqlalchemy import extract
from app.database import SessionLocal
from app.models.transaction import Transaction
from app.state.session import get_current_user


# =========================
# CREAR TRANSACCIÓN
# =========================
def add_transaction(t_type, amount, category, description=None, date=None):
    db = SessionLocal()
    try:
        user = get_current_user()
        user_id = user.id if user else None

        tx = Transaction(
            user_id=user_id,
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
def list_transactions(limit=100, user_id=None):
    db = SessionLocal()
    try:
        if user_id is None:
            user = get_current_user()
            user_id = user.id if user else None

        q = db.query(Transaction)
        if user_id is not None:
            q = q.filter(Transaction.user_id == user_id)

        return (
            q.order_by(Transaction.date.desc(), Transaction.id.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()


# =========================
# LISTAR POR MES / AÑO
# =========================
def list_transactions_by_month(year, month, user_id=None):
    db = SessionLocal()
    try:
        if user_id is None:
            user = get_current_user()
            user_id = user.id if user else None

        q = db.query(Transaction)
        q = q.filter(extract("year", Transaction.date) == year)
        q = q.filter(extract("month", Transaction.date) == month)

        if user_id is not None:
            q = q.filter(Transaction.user_id == user_id)

        return q.order_by(Transaction.date.desc(), Transaction.id.desc()).all()
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

        # check ownership
        user = get_current_user()
        if user and tx.user_id != user.id:
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

        user = get_current_user()
        if user and tx.user_id != user.id:
            return

        db.delete(tx)
        db.commit()
    finally:
        db.close()
