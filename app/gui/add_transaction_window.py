import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date

from tkcalendar import DateEntry
from app.services.expenses import add_transaction, list_transactions


class AddTransactionWindow(tk.Toplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)

        self.on_save = on_save

        self.title("Añadir transacción")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        # =========================
        # Variables
        # =========================
        self.type_var = tk.StringVar(value="Ingreso")
        self.amount_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()

        # =========================
        # Contenedor principal
        # =========================
        container = ttk.Frame(self, padding=15)
        container.grid(row=0, column=0, sticky="nsew")

        # =========================
        # Tipo
        # =========================
        ttk.Label(container, text="Tipo").grid(row=0, column=0, sticky="w")
        type_combo = ttk.Combobox(
            container,
            textvariable=self.type_var,
            values=["Ingreso", "Gasto"],
            state="readonly"
        )
        type_combo.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        type_combo.bind("<<ComboboxSelected>>", lambda e: self.update_categories())

        # =========================
        # Fecha
        # =========================
        ttk.Label(container, text="Fecha").grid(row=2, column=0, sticky="w")
        self.date_entry = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.date_entry.set_date(date.today())
        self.date_entry.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # =========================
        # Categoría
        # =========================
        ttk.Label(container, text="Categoría").grid(row=4, column=0, sticky="w")
        self.category_combo = ttk.Combobox(
            container,
            textvariable=self.category_var
        )
        self.category_combo.grid(row=5, column=0, sticky="ew", pady=(0, 10))

        # =========================
        # Importe
        # =========================
        ttk.Label(container, text="Importe (€)").grid(row=6, column=0, sticky="w")
        ttk.Entry(
            container,
            textvariable=self.amount_var
        ).grid(row=7, column=0, sticky="ew", pady=(0, 10))

        # =========================
        # Descripción
        # =========================
        ttk.Label(container, text="Descripción").grid(row=8, column=0, sticky="w")
        ttk.Entry(
            container,
            textvariable=self.description_var
        ).grid(row=9, column=0, sticky="ew", pady=(0, 15))

        # =========================
        # Botones
        # =========================
        buttons = ttk.Frame(container)
        buttons.grid(row=10, column=0, sticky="e")

        ttk.Button(
            buttons,
            text="Cancelar",
            command=self.destroy
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            buttons,
            text="💾 Guardar",
            command=self.save_transaction
        ).grid(row=0, column=1)

        # Ajustes finales
        container.columnconfigure(0, weight=1)

        self.update_categories()
        self._fix_window_size(parent)

    # =========================
    # Fix tamaño ventana (CRÍTICO)
    # =========================
    def _fix_window_size(self, parent):
        self.update_idletasks()

        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()

        x = parent.winfo_rootx() + (parent.winfo_width() // 2) - (width // 2)
        y = parent.winfo_rooty() + (parent.winfo_height() // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

    # =========================
    # Lógica
    # =========================
    def update_categories(self):
        transactions = list_transactions(limit=1000)
        categories = set()

        selected_type = self.type_var.get().lower()

        for tx in transactions:
            if tx.type == selected_type and tx.category:
                categories.add(tx.category)

        self.category_combo["values"] = sorted(categories)

    def save_transaction(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "El importe no es válido")
            return

        t_type = self.type_var.get().lower()

        if t_type == "gasto" and amount > 0:
            amount = -amount
        elif t_type == "ingreso" and amount < 0:
            amount = abs(amount)

        category = self.category_var.get().strip()
        if not category:
            messagebox.showerror("Error", "La categoría es obligatoria")
            return

        add_transaction(
            t_type=t_type,
            amount=amount,
            category=category,
            description=self.description_var.get().strip(),
            date=self.date_entry.get_date()
        )

        if self.on_save:
            self.on_save()

        self.destroy()