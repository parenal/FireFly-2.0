import tkinter as tk
from tkinter import ttk, messagebox
from app.gui.transactions_view import TransactionsView


class MainWindow:
    def __init__(self, root, on_logout=None):
        self.root = root
        self.on_logout = on_logout
        root.title("FireFly 2.0 - Control de gastos")
        root.geometry("800x500")

        # Menu de cuenta (cerrar sesión)
        menubar = tk.Menu(root)
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Cambiar contraseña", command=self._on_change_password)
        account_menu.add_separator()
        account_menu.add_command(label="Cerrar sesión", command=self._on_logout)
        menubar.add_cascade(label="Cuenta", menu=account_menu)
        root.config(menu=menubar)

        # Indicador de usuario (esquina superior derecha)
        try:
            from app.state.session import get_current_user
            user = get_current_user()
            username = user.username if user else ""
        except Exception:
            username = ""

        self.user_label = ttk.Label(root, text=f"Usuario: {username}")
        self.user_label.place(relx=1.0, x=-10, y=6, anchor="ne")

        style = ttk.Style()
        style.theme_use("default")

        self.app = TransactionsView(root)
        self.app.pack(fill="both", expand=True)

    def _on_logout(self):
        if not messagebox.askyesno("Confirmar", "¿Cerrar sesión?"):
            return

        if self.on_logout:
            try:
                self.on_logout()
            except Exception:
                pass
        else:
            # Fallback: limpiar sesión y mostrar login
            try:
                from app.state.session import clear_current_user
                from app.gui.login_window import LoginWindow
            except Exception:
                return

            clear_current_user()
            try:
                self.app.destroy()
            except Exception:
                pass
            self.root.withdraw()
            LoginWindow(self.root)
        # update user label
        try:
            self.user_label.config(text="Usuario: ")
        except Exception:
            pass

    def _on_change_password(self):
        try:
            from app.gui.change_password_window import ChangePasswordWindow
        except Exception:
            return

        ChangePasswordWindow(self.root)

    def close(self):
        try:
            self.app.destroy()
        except Exception:
            pass