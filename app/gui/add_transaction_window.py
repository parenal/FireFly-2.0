import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date

from app.services.expenses import add_transaction, list_transactions


class AddTransactionWindow(tk.Toplevel):
    def __init__(self, parent, on_save=None):
        super().__init__(parent)

        self.on_save = on_save

        # =========================
        # Ventana
        # =========================
        self.title("Añadir transacción")
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)

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
        container = ttk.Frame(self, padding=(20, 20, 20, 30))
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
        type_combo.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        type_combo.bind("<<ComboboxSelected>>", self.update_categories)

        # =========================
        # Fecha
        # =========================
        ttk.Label(container, text="Fecha").grid(row=2, column=0, sticky="w")
        self.date_entry = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.date_entry.set_date(date.today())
        self.date_entry.grid(row=3, column=0, sticky="ew", pady=(0, 12))

        # =========================
        # Categoría
        # =========================
        ttk.Label(container, text="Categoría").grid(row=4, column=0, sticky="w")
        self.category_combo = ttk.Combobox(
            container,
            textvariable=self.category_var
        )
        self.category_combo.grid(row=5, column=0, sticky="ew", pady=(0, 12))

        # =========================
        # Importe
        # =========================
        ttk.Label(container, text="Importe (€)").grid(row=6, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.amount_var)\
            .grid(row=7, column=0, sticky="ew", pady=(0, 12))

        # =========================
        # Descripción
        # =========================
        ttk.Label(container, text="Descripción").grid(row=8, column=0, sticky="w")
        ttk.Entry(container, textvariable=self.description_var)\
            .grid(row=9, column=0, sticky="ew", pady=(0, 18))

        # =========================
        # Botones (MARGEN REAL)
        # =========================
        buttons = ttk.Frame(container)
        buttons.grid(row=10, column=0, pady=(0, 10))

        ttk.Button(
            buttons,
            text="Guardar",
            command=self.save_transaction
        ).grid(row=0, column=0, padx=10)

        ttk.Button(
            buttons,
            text="Cancelar",
            command=self.destroy
        ).grid(row=0, column=1, padx=10)

        # =========================
        # Grid config
        # =========================
        container.columnconfigure(0, weight=1)

        # =========================
        # Categorías iniciales
        # =========================
        self.update_categories()

        # =========================
        # Forzar cálculo real
        # =========================
        self.update_idletasks()

        # Tamaño mínimo REAL (clave)
        self.minsize(
            self.winfo_reqwidth(),
            self.winfo_reqheight() + 10
        )

        # Centrar ventana
        x = (self.winfo_screenwidth() // 2) - (self.winfo_reqwidth() // 2)
        y = (self.winfo_screenheight() // 2) - (self.winfo_reqheight() // 2)
        self.geometry(f"+{x}+{y}")

    # =========================
    # Categorías dinámicas
    # =========================
    def update_categories(self, event=None):
        tx_type = "income" if self.type_var.get() == "Ingreso" else "expense"

        transactions = get_all_transactions()

        categories = sorted({
            tx.category
            for tx in transactions
            if tx.type == tx_type and tx.category
        })

        self.category_combo["values"] = categories

    # =========================
    # Guardar
    # =========================
    def save_transaction(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            messagebox.showerror("Error", "El importe debe ser un número válido")
            return

        if not self.category_var.get():
            messagebox.showerror("Error", "La categoría es obligatoria")
            return

        t_type = "income" if self.type_var.get() == "Ingreso" else "expense"

        if t_type == "expense" and amount > 0:
            amount = -amount
        elif t_type == "income" and amount < 0:
            amount = abs(amount)

        add_transaction(
            t_type=t_type,
            amount=amount,
            category=self.category_var.get(),
            description=self.description_var.get(),
            date=self.date_entry.get_date()
        )

        if self.on_save:
            self.on_save()

        self.destroy()
