import matplotlib.pyplot as plt
import pandas as pd
from app.services.reports import get_transactions_df
import numpy as np

def plot_category_expenses():
    df = get_transactions_df()

    # Filtramos solo gastos
    expenses = df[df["type"] == "expense"]

    if expenses.empty:
        print("No hay gastos para graficar")
        return

    # Sumamos por categoría
    summary = expenses.groupby("category")["amount"].sum().sort_values(ascending=False)

    # Ajustar tamaño de la figura según número de categorías
    plt.figure(figsize=(max(8, len(summary)*1.2), 6))

    # Gradiente de colores para las barras
    colors = plt.cm.Oranges(np.linspace(0.5, 1, len(summary)))

    bars = plt.bar(summary.index, summary.values, color=colors)

    # Añadir etiquetas encima de cada barra
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width()/2, 
            height + 0.2, 
            f"{height:.2f}€", 
            ha='center', va='bottom', fontsize=9
        )

    # Ticks y rotación
    max_y = summary.max()
    plt.yticks(np.arange(0, max_y + 2, 2))   # ticks cada 2€
    plt.xticks(rotation=45, ha="right")

    # Títulos y etiquetas
    plt.title("Gastos por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Importe (€)")

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
