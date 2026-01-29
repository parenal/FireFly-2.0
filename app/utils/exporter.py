import matplotlib.pyplot as plt
import pandas as pd
from app.services.reports import get_transactions_df
import numpy as np


def export_category_chart(path: str, start_date=None, end_date=None):
    df = get_transactions_df()
    if start_date is not None:
        df = df[pd.to_datetime(df["date"]) >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[pd.to_datetime(df["date"]) <= pd.to_datetime(end_date)]

    expenses = df[df["type"] == "expense"]
    if expenses.empty:
        raise ValueError("No hay gastos para exportar")

    summary = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)

    plt.figure(figsize=(max(8, len(summary)*1.2), 6))
    colors = plt.cm.Oranges(np.linspace(0.5, 1, len(summary)))
    bars = plt.bar(summary.index, summary.values, color=colors)
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 0.2, f"{height:.2f}€", ha='center', va='bottom', fontsize=9)

    plt.xticks(rotation=45, ha="right")
    plt.title("Gastos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Importe (€)")
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def export_monthly_chart(path: str, start_date=None, end_date=None):
    df = get_transactions_df()
    if start_date is not None:
        df = df[pd.to_datetime(df["date"]) >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[pd.to_datetime(df["date"]) <= pd.to_datetime(end_date)]

    if df.empty:
        raise ValueError("No hay transacciones para exportar")

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    income_month = df[df["type"]=="income"].groupby("month")["amount"].sum()
    expense_month = df[df["type"]=="expense"].groupby("month")["amount"].sum()

    plt.figure(figsize=(10,5))
    plt.plot(income_month.index.astype(str), income_month.values, label="Ingresos", marker='o', color="green")
    plt.plot(expense_month.index.astype(str), expense_month.values, label="Gastos", marker='o', color="red")
    plt.title("Evolución mensual")
    plt.xlabel("Mes")
    plt.ylabel("Importe (€)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def export_transactions_excel(path: str, start_date=None, end_date=None):
    df = get_transactions_df()
    if start_date is not None:
        df = df[pd.to_datetime(df["date"]) >= pd.to_datetime(start_date)]
    if end_date is not None:
        df = df[pd.to_datetime(df["date"]) <= pd.to_datetime(end_date)]
    if df.empty:
        raise ValueError("No hay datos para exportar")
    # Ensure date type
    try:
        df["date"] = pd.to_datetime(df["date"])
    except Exception:
        pass

    # reorder columns
    cols = [c for c in ["date", "type", "amount", "category"] if c in df.columns]
    # Try to write Excel using openpyxl; if missing, fall back to CSV
    try:
        import openpyxl  # noqa: F401
        df.to_excel(path, index=False, columns=cols)
        return path
    except ImportError:
        # fallback to CSV
        if path.lower().endswith('.xlsx'):
            csv_path = path[:-5] + '.csv'
        else:
            csv_path = path + '.csv'
        df.to_csv(csv_path, index=False, columns=cols)
        return csv_path
    except Exception:
        # propagate other exceptions
        raise
