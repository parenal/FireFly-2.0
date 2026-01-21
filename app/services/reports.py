import pandas as pd
from app.database import SessionLocal
from app.models import Transaction

def get_transactions_df():
    session = SessionLocal()
    data = session.query(Transaction).all()
    session.close()

    df = pd.DataFrame([{
        "date": t.date,
        "type": t.type,
        "amount": t.amount,
        "category": t.category
    } for t in data])

    return df
def total_balance():
    df = get_transactions_df()

    income = df[df["type"] == "income"]["amount"].sum()
    expense = df[df["type"] == "expense"]["amount"].sum()

    return income - expense, income, expense
def monthly_summary(year: int, month: int):
    df = get_transactions_df()

    df["date"] = pd.to_datetime(df["date"])
    monthly = df[
        (df["date"].dt.year == year) &
        (df["date"].dt.month == month)
    ]

    income = monthly[monthly["type"] == "income"]["amount"].sum()
    expense = monthly[monthly["type"] == "expense"]["amount"].sum()

    return income, expense, income - expense
