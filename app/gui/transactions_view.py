import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.services.expenses import (
    list_transactions,
    list_transactions_by_month,
    delete_transaction
)
from app.gui.add_transaction_window import AddTransactionWindow


class TransactionsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        # =========================
        # MESES
        # =========================
        self.months = {
            "Enero": 1,
            "Febrero": 2,
            "Marzo": 3,
            "Abril": 4,
            "Mayo": 5,
            "Junio": 6,
            "Julio": 7,
            "Agosto": 8,
            "Septiembre": 9,
            "Octubre": 10,
            "Noviembre": 11,
            "Diciembre": 12,
        }

        now = datetime.now()
        self.selected_month = tk.StringVar()
        self.selected_year = tk.IntVar()

        self.selected_month.set(list(self.months.keys())[now.month - 1])
        self.selected_year.set(now.year)

        # =========================
        # FILTROS SUPERIORES
        # =========================
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Mes:").pack(side="left", padx=5)

        month_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.selected_month,
            values=list(self.months.keys()),
            state="readonly",
            width=12
        )
        month_cb.pack(side="left")

        ttk.Label(filter_frame, text="Año:").pack(side="left", padx=5)

        years = list(range(now.year - 5, now.year + 1))
        year_cb = ttk.Combobox(
            filter_frame,
            textvariable=self.selected_year,
            values=years,
            state="readonly",
            width=6
        )
        year_cb.pack(side="left")

        month_cb.bind("<<ComboboxSelected>>", lambda e: self.load_transactions())
        year_cb.bind("<<ComboboxSelected>>", lambda e: self.load_transactions())

        # =========================
        # TABLA
        # =========================
        columns = ("id", "type", "amount", "category", "description", "date")

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("amount", text="Importe")
        self.tree.heading("category", text="Categoría")
        self.tree.heading("description", text="Descripción")
        self.tree.heading("date", text="Fecha")

        self.tree.bind("<Button-3>", self.show_context_menu)

        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Editar", command=self.edit_transaction)
        self.context_menu.add_command(label="Eliminar", command=self.delete_transaction)

        self.load_transactions()

    # =========================
    # CARGAR TRANSACCIONES
    # =========================
    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        month_name = self.selected_month.get()
        year = self.selected_year.get()

        month = self.months.get(month_name)
        transactions = list_transactions_by_month(year, month)

        for tx in transactions:
            self.tree.insert(
                "",
                "end",
                values=(
                    tx.id,
                    tx.type,
                    tx.amount,
                    tx.category,
                    tx.description,
                    tx.date.strftime("%d/%m/%Y"),
                )
            )

    # =========================
    # MENÚ CONTEXTUAL
    # =========================
    def show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    # =========================
    # EDITAR
    # =========================
    def edit_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        tx_id = values[0]

        AddTransactionWindow(
            self,
            transaction_id=tx_id,
            on_save=self.load_transactions
        )

    # =========================
    # ELIMINAR
    # =========================
    def delete_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        tx_id = values[0]

        if messagebox.askyesno("Confirmar", "¿Eliminar esta transacción?"):
            delete_transaction(tx_id)
            self.load_transactions()
