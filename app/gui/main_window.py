import tkinter as tk
from tkinter import ttk
from app.gui.transactions_view import TransactionsView

def run_app():
    root = tk.Tk()
    root.title("FireFly 2.0 - Control de gastos")
    root.geometry("800x500")

    style = ttk.Style()
    style.theme_use("default")

    app = TransactionsView(root)
    app.pack(fill="both", expand=True)

    root.mainloop()