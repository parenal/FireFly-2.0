import matplotlib.pyplot as plt
import pandas as pd
from app.services.reports import get_transactions_df

def plot_category_expenses():
    df = get_transactions_df()

    # Filtramos solo gastos
    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("No hay gastos para graficar")
        return

    # Sumamos por categoría
    summary = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)

    # Gráfica de barras
    summary.plot(kind="bar", color="tomato")
    plt.title("Gastos por categoría")
    plt.ylabel("Importe (€)")
    plt.xlabel("Categoría")
    plt.tight_layout()
    plt.show()


def plot_monthly_evolution():
    df = get_transactions_df()
    if df.empty:
        print("No hay transacciones para graficar")
        return

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    # Sumamos ingresos y gastos por mes
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
    plt.show()
