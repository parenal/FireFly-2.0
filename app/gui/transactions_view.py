import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from app.gui.add_transaction_window import AddTransactionWindow
from app.gui.edit_transaction_window import EditTransactionWindow
from app.services.expenses import list_transactions, delete_transaction


class TransactionsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # =========================
        # Variables mes / año
        # =========================
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()

        # =========================
        # Estilo botón +
        # =========================
        style = ttk.Style()
        style.configure(
            "Add.TButton",
            font=("Segoe UI", 14, "bold"),
            padding=(10, 6)
        )

        # =========================
        # Filtro superior
        # =========================
        filter_frame = ttk.Frame(self)
        filter_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(filter_frame, text="Mes:").pack(side="left")

        self.month_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.month_var,
            state="readonly",
            width=12
        )
        self.month_combo.pack(side="left", padx=(5, 15))

        ttk.Label(filter_frame, text="Año:").pack(side="left")

        self.year_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.year_var,
            state="readonly",
            width=8
        )
        self.year_combo.pack(side="left", padx=(5, 15))

        # Espaciador
        ttk.Frame(filter_frame).pack(side="left", expand=True)

        # =========================
        # Botón +
        # =========================
        add_btn = ttk.Button(
            filter_frame,
            text="+",
            style="Add.TButton",
            command=self.add_transaction
        )
        add_btn.pack(side="right")

        # Tooltip
        self._add_tooltip(add_btn, "Añadir transacción")

        # =========================
        # Tabla
        # =========================
        columns = ("id", "type", "amount", "category")

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("amount", text="Importe")
        self.tree.heading("category", text="Categoría")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("type", width=120, anchor="center")
        self.tree.column("amount", width=120, anchor="center")
        self.tree.column("category", width=200)

        self.tree.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # =========================
        # Menú contextual
        # =========================
        self.menu = tk.Menu(self, tearoff=0)
        self.menu.add_command(label="Editar", command=self.edit_transaction)
        self.menu.add_command(label="Eliminar", command=self.delete_transaction)

        self.tree.bind("<Button-3>", self.show_context_menu)

        # =========================
        # Eventos
        # =========================
        self.month_combo.bind("<<ComboboxSelected>>", lambda e: self.load_transactions())
        self.year_combo.bind("<<ComboboxSelected>>", lambda e: self.load_transactions())

        self._load_months_years()
        self.load_transactions()

    # ======================================================
    # Cargar meses y años
    # ======================================================
    def _load_months_years(self):
        months = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]

        now = datetime.now()
        self.month_combo["values"] = months
        self.month_var.set(months[now.month - 1])

        years = [str(y) for y in range(now.year - 5, now.year + 2)]
        self.year_combo["values"] = years
        self.year_var.set(str(now.year))

    # ======================================================
    # Cargar transacciones
    # ======================================================
    def load_transactions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        month_index = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ].index(self.month_var.get()) + 1

        year = int(self.year_var.get())

        transactions = list_transactions(limit=1000)

        for tx in transactions:
            if tx.date.month == month_index and tx.date.year == year:
                self.tree.insert("", "end", values=(
                    tx.id,
                    tx.type.capitalize(),
                    f"{tx.amount:.2f}",
                    tx.category
                ))

    # ======================================================
    # Acciones
    # ======================================================
    def add_transaction(self):
        AddTransactionWindow(self, on_save=self.load_transactions)

    def edit_transaction(self):
        tx = self.get_selected_transaction()
        if not tx:
            return

        EditTransactionWindow(
            parent=self,
            transaction=tx,
            on_save=self.load_transactions
        )

    def delete_transaction(self):
        tx = self.get_selected_transaction()
        if not tx:
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar esta transacción?"):
            return

        delete_transaction(tx.id)
        self.load_transactions()

    # ======================================================
    # Utilidades
    # ======================================================
    def get_selected_transaction(self):
        selected = self.tree.selection()
        if not selected:
            return None

        item = self.tree.item(selected[0])
        tx_id = item["values"][0]

        transactions = list_transactions(limit=1000)
        for tx in transactions:
            if tx.id == tx_id:
                return tx

        return None

    def show_context_menu(self, event):
        row = self.tree.identify_row(event.y)
        if row:
            self.tree.selection_set(row)
            self.menu.tk_popup(event.x_root, event.y_root)

    def _add_tooltip(self, widget, text):
        tooltip = tk.Toplevel(widget)
        tooltip.withdraw()
        tooltip.overrideredirect(True)

        label = ttk.Label(
            tooltip,
            text=text,
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            padding=4
        )
        label.pack()

        def show(event):
            tooltip.geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            tooltip.deiconify()

        def hide(event):
            tooltip.withdraw()

        widget.bind("<Enter>", show)
        widget.bind("<Leave>", hide)
