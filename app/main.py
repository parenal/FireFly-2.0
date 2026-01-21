import typer
from rich.console import Console

from app.services.expenses import add_transaction
from app.cli import show_transactions
from app.services.reports import total_balance, monthly_summary
from app.services.graphs import plot_category_expenses, plot_monthly_evolution

app = typer.Typer()
console = Console()

# ---------- COMANDOS EXISTENTES ----------

@app.command()
def add(
    t_type: str = typer.Option(..., help="income o expense"),
    amount: float = typer.Option(...),
    category: str = typer.Option(...),
    description: str = typer.Option(None)
):
    add_transaction(t_type, amount, category, description)
    typer.echo("✔ Transacción añadida")


@app.command()
def list(
    limit: int = typer.Option(10, help="Número de registros a mostrar")
):
    show_transactions(limit)


@app.command()
def balance():
    total, income, expense = total_balance()
    console.print(f"[green]Ingresos:[/green] {income:.2f} €")
    console.print(f"[red]Gastos:[/red] {expense:.2f} €")
    console.print(f"[bold]Balance total:[/bold] {total:.2f} €")


@app.command()
def month(
    year: int = typer.Option(...),
    month: int = typer.Option(...)
):
    income, expense, balance = monthly_summary(year, month)
    console.print(f"[green]Ingresos:[/green] {income:.2f} €")
    console.print(f"[red]Gastos:[/red] {expense:.2f} €")
    console.print(f"[bold]Balance:[/bold] {balance:.2f} €")


# ---------- NUEVOS COMANDOS DE GRAFICAS ----------

@app.command()
def graph_category():
    """Mostrar gráfica de gastos por categoría"""
    plot_category_expenses()


@app.command()
def graph_monthly():
    """Mostrar gráfica de evolución mensual"""
    plot_monthly_evolution()


# ---------- LLAMADA FINAL A LA APP ----------
if __name__ == "__main__":
    app()
