import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

from app.services.expenses import add_transaction
from app.database import SessionLocal
from app.models import Transaction


class AddTransactionWindow(tk.Toplevel):
    def __init__(self, parent, on_save):
        super().__init__(parent)
        self.on_save = on_save

        self.title("Añadir transacción")
        self.geometry("400x420")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        frame = ttk.Frame(self, padding=15)
        frame.pack(fill="both", expand=True)

        # Tipo de transacción
        ttk.Label(frame, text="Tipo").pack(anchor="w")
        self.type_var = tk.StringVar(value="Gasto")
        type_combo = ttk.Combobox(
            frame,
            textvariable=self.type_var,
            values=["Gasto", "Ingreso"],
            state="readonly"
        )
        type_combo.pack(fill="x", pady=5)

        # Fecha (calendario)
        ttk.Label(frame, text="Fecha").pack(anchor="w")
        self.date_entry = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            locale="es_ES"
        )
        self.date_entry.pack(fill="x", pady=5)

        # Categoría (con memoria)
        ttk.Label(frame, text="Categoría").pack(anchor="w")
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(
            frame,
            textvariable=self.category_var
        )
        self.category_combo.pack(fill="x", pady=5)
        self.load_categories()

        # Cantidad
        ttk.Label(frame, text="Cantidad (€)").pack(anchor="w")
        self.amount_entry = ttk.Entry(frame)
        self.amount_entry.pack(fill="x", pady=5)

        # Descripción
        ttk.Label(frame, text="Descripción").pack(anchor="w")
        self.desc_entry = ttk.Entry(frame)
        self.desc_entry.pack(fill="x", pady=5)

        # Botones
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)

        ttk.Button(
            btn_frame,
            text="Guardar",
            command=self.save
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="Cancelar",
            command=self.destroy
        ).pack(side="left", padx=5)

    def load_categories(self):
        session = SessionLocal()
        categories = session.query(Transaction.category).distinct().all()
        session.close()

        self.category_combo["values"] = [c[0] for c in categories]

    def save(self):
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                raise ValueError

            tipo_ui = self.type_var.get()
            t_type = "income" if tipo_ui == "Ingreso" else "expense"

            add_transaction(
                t_type=t_type,
                amount=amount,
                category=self.category_var.get(),
                description=self.desc_entry.get(),
                date=self.date_entry.get_date()
            )

            self.on_save()
            self.destroy()

        except ValueError:
            messagebox.showerror(
                "Error",
                "La cantidad debe ser un número positivo"
            )