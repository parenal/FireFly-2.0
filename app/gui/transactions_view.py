import tkinter as tk
from tkinter import ttk, messagebox

from app.gui.add_transaction_window import AddTransactionWindow
from app.services.expenses import (
    list_transactions,
    delete_transaction
)


class TransactionsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # =========================
        # Estilos
        # =========================
        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        # =========================
        # Título
        # =========================
        ttk.Label(
            self,
            text="Transacciones",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        # =========================
        # Tabla
        # =========================
        columns = ("fecha", "tipo", "categoria", "importe", "descripcion")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        for col, text, width, anchor in [
            ("fecha", "Fecha", 100, "center"),
            ("tipo", "Tipo", 100, "center"),
            ("categoria", "Categoría", 150, "w"),
            ("importe", "Importe (€)", 100, "e"),
            ("descripcion", "Descripción", 250, "w"),
        ]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor=anchor)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # =========================
        # Menú contextual
        # =========================
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(
            label="✏️ Editar transacción",
            command=self.edit_transaction
        )
        self.menu.add_command(
            label="🗑 Eliminar transacción",
            command=self.delete_transaction
        )

        self.tree.bind("<Button-3>", self.show_context_menu)

        # =========================
        # Botón añadir
        # =========================
        ttk.Button(
            self,
            text="➕ Añadir transacción",
            command=self.open_add_transaction_window
        ).pack(pady=(0, 10))

        # =========================
        # Datos
        # =========================
        self.transactions = []
        self.load_transactions()

    # =========================
    # Cargar datos
    # =========================
    def load_transactions(self):
        self.tree.delete(*self.tree.get_children())

        self.transactions = list_transactions(limit=100)

        for tx in self.transactions:
            tipo = "Ingreso" if tx.type == "income" else "Gasto"
            categoria = tx.category or ""

            self.tree.insert(
                "",
                "end",
                iid=str(tx.id),
                values=(
                    tx.date,
                    tipo,
                    categoria,
                    f"{tx.amount:.2f}",
                    tx.description or ""
                )
            )

    # =========================
    # Click derecho
    # =========================
    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return

        self.tree.selection_set(row_id)
        self.menu.tk_popup(event.x_root, event.y_root)

    # =========================
    # Editar
    # =========================
    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return

        tx_id = int(selected[0])
        tx = next(t for t in self.transactions if t.id == tx_id)

        AddTransactionWindow(
            self,
            transaction=tx,
            on_save=self.load_transactions
        )

    # =========================
    # Eliminar
    # =========================
    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return

        tx_id = int(selected[0])

        if not messagebox.askyesno(
            "Confirmar",
            "¿Seguro que quieres eliminar esta transacción?"
        ):
            return

        delete_transaction(tx_id)
        self.load_transactions()

    # =========================
    # Añadir
    # =========================
    def open_add_transaction_window(self):
        AddTransactionWindow(self, on_save=self.load_transactions)
