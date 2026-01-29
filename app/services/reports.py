import pandas as pd
from app.database import SessionLocal
from app.models.transaction import Transaction
from app.state.session import get_current_user


def get_transactions_df():
    session = SessionLocal()
    user = get_current_user()
    if user:
        data = session.query(Transaction).filter(Transaction.user_id == user.id).all()
    else:
        data = session.query(Transaction).all()

    session.close()

    df = pd.DataFrame([{
        "date": t.date,
        "type": t.type,
        "amount": t.amount,
        "category": t.category
    } for t in data])

    # Normalize type values to 'income'/'expense' for reporting/graphs compatibility
    if not df.empty and "type" in df.columns:
        def _norm_type(v):
            try:
                s = str(v).strip().lower()
            except Exception:
                return v
            if s in ("gasto", "expense", "egreso"):
                return "expense"
            if s in ("ingreso", "income"):
                return "income"
            return s

        df["type"] = df["type"].apply(_norm_type)

    return df
def total_balance():
    df = get_transactions_df()
    if df.empty or "type" not in df.columns or "amount" not in df.columns:
        return 0.0, 0.0, 0.0

    income = df[df["type"] == "income"]["amount"].sum()
    # expenses may be stored as negative amounts; take absolute values
    expense = df[df["type"] == "expense"]["amount"].abs().sum()

    return income - expense, income, expense
def monthly_summary(year: int, month: int):
    df = get_transactions_df()
    # if no data or date/amount/type columns missing, return zeros
    if df.empty or "date" not in df.columns or "type" not in df.columns or "amount" not in df.columns:
        return 0.0, 0.0, 0.0

    df["date"] = pd.to_datetime(df["date"])
    monthly = df[
        (df["date"].dt.year == year) &
        (df["date"].dt.month == month)
    ]

    income = monthly[monthly["type"] == "income"]["amount"].sum()
    expense = monthly[monthly["type"] == "expense"]["amount"].abs().sum()

    return income, expense, income - expense

def annual_summary(year: int):
    df = get_transactions_df()
    if df.empty:
        return 0.0, 0.0, 0.0
    df["date"] = pd.to_datetime(df["date"])
    yearly = df[df["date"].dt.year == int(year)]
    income = yearly[yearly["type"] == "income"]["amount"].sum()
    expense = yearly[yearly["type"] == "expense"]["amount"].abs().sum()
    return income, expense, income - expense


def monthly_balances(year: int):
    """Return list of (month, income, expense, net) for months 1..12 for a given year."""
    df = get_transactions_df()
    months = []
    if df.empty:
        for m in range(1, 13):
            months.append((m, 0.0, 0.0, 0.0))
        return months

    df["date"] = pd.to_datetime(df["date"])
    for m in range(1, 13):
        monthly = df[(df["date"].dt.year == int(year)) & (df["date"].dt.month == m)]
        income = monthly[monthly["type"] == "income"]["amount"].sum()
        expense = monthly[monthly["type"] == "expense"]["amount"].abs().sum()
        months.append((m, income, expense, income - expense))
    return months
