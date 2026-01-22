import tkinter as tk
from tkinter import ttk

from app.database import SessionLocal
from app.models import Transaction
from app.gui.add_transaction_window import AddTransactionWindow


class TransactionsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):
        # Título
        title = ttk.Label(self, text="Transacciones", font=("Segoe UI", 16))
        title.pack(pady=10)

        # Tabla
        columns = ("date", "type", "category", "amount", "description")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        self.tree.heading("date", text="Fecha")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("category", text="Categoría")
        self.tree.heading("amount", text="Importe (€)")
        self.tree.heading("description", text="Descripción")

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Frame de botones (AHORA ABAJO)
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        add_btn = ttk.Button(
            button_frame,
            text="➕ Añadir transacción",
            command=self.open_add_transaction
        )
        add_btn.pack()

    def load_transactions(self):
        session = SessionLocal()
        transactions = session.query(Transaction).order_by(Transaction.date.desc()).all()

        for tx in transactions:
            tipo_es = "Ingreso" if tx.type == "income" else "Gasto"

            self.tree.insert(
                "",
                "end",
                values=(
                    tx.date.strftime("%Y-%m-%d"),
                    tipo_es,
                    tx.category,
                    f"{tx.amount:.2f}",
                    tx.description or ""
                )
            )

        session.close()

    def reload(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.load_transactions()

    def open_add_transaction(self):
        AddTransactionWindow(self, on_save=self.reload)
