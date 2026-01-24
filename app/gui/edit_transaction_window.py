import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from tkcalendar import DateEntry
from app.services.expenses import update_transaction, list_transactions


class EditTransactionWindow(tk.Toplevel):
    def __init__(self, parent, transaction, on_save=None):
        super().__init__(parent)

        self.transaction = transaction
        self.on_save = on_save

        self.title("Editar transacción")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # =========================
        # Variables
        # =========================
        self.type_var = tk.StringVar(value=transaction.type.capitalize())
        self.amount_var = tk.StringVar(value=str(abs(transaction.amount)))
        self.category_var = tk.StringVar(value=transaction.category)
        self.description_var = tk.StringVar(value=transaction.description or "")

        # =========================
        # Contenedor
        # =========================
        container = ttk.Frame(self, padding=15)
        container.grid(row=0, column=0, sticky="nsew")

        # Tipo
        ttk.Label(container, text="Tipo").grid(row=0, column=0, sticky="w")
        type_combo = ttk.Combobox(
            container,
            textvariable=self.type_var,
            values=["Ingreso", "Gasto"],
            state="readonly"
        )
        type_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_categories())

        # Fecha
        ttk.Label(container, text="Fecha").grid(row=2, column=0, sticky="w")
        self.date_entry = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.date_entry.set_date(transaction.date)
        self.date_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # Categoría
        ttk.Label(container, text="Categoría").grid(row=4, column=0, sticky="w")
        self.category_combo = ttk.Combobox(container, textvariable=self.category_var)
        self.category_combo.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # Importe
        ttk.Label(container, text="Importe (€)").grid(row=6, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.amount_var)\
            .grid(row=7, column=0, sticky="ew", pady=(0, 10))

        # Descripción
        ttk.Label(container, text="Descripción").grid(row=8, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.description_var)\
            .grid(row=9, column=0, sticky="ew", pady=(0, 15))

        # Botones
        buttons = ttk.Frame(container)
        buttons.grid(row=10, column=0, sticky="e")

        ttk.Button(buttons, text="Cancelar", command=self.destroy)\
            .grid(row=0, column=0, padx=5)

        ttk.Button(buttons, text="💾 Guardar cambios", command=self.save_changes)\
            .grid(row=0, column=1)

        container.columnconfigure(0, weight=1)

        self.update_categories()
        self._fix_window_size(parent)

    # =========================
    def _fix_window_size(self, parent):
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - w // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - h // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # =========================
    def update_categories(self):
        transactions = list_transactions(limit=1000)
        categories = {
            tx.category for tx in transactions
            if tx.type == self.type_var.get().lower()
        }
        self.category_combo["values"] = sorted(categories)

    # =========================
    def save_changes(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "Importe no válido")
            return

        t_type = self.type_var.get().lower()
        if t_type == "gasto":
            amount = -abs(amount)
        else:
            amount = abs(amount)

        update_transaction(
            transaction_id=self.transaction.id,
            t_type=t_type,
            amount=amount,
            category=self.category_var.get().strip(),
            description=self.description_var.get().strip(),
            date=self.date_entry.get_date()
        )

        if self.on_save:
            self.on_save()

        self.destroy()