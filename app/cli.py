from rich.console import Console
from rich.table import Table
from app.services.expenses import list_transactions

console = Console()

def show_transactions(limit=20):
    transactions = list_transactions(limit)

    table = Table(title="Últimas transacciones")

    table.add_column("ID", justify="right")
    table.add_column("Fecha")
    table.add_column("Tipo")
    table.add_column("Categoría")
    table.add_column("Importe", justify="right")
    table.add_column("Descripción")

    for tx in transactions:
        table.add_row(
            str(tx.id),
            str(tx.date),
            tx.type,
            tx.category,
            f"{tx.amount:.2f} €",
            tx.description or ""
        )

    console.print(table)
