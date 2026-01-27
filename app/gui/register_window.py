import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import create_user


class RegisterWindow(tk.Toplevel):
    def __init__(self, login_window):
        super().__init__(login_window)

        self.login_window = login_window

        self.title("Registro")
        self.geometry("320x300")
        self.resizable(False, False)

        fields = [
            ("Usuario", "username"),
            ("Nombre", "name"),
            ("Apellido", "surname"),
            ("Contraseña", "password"),
        ]

        self.entries = {}

        for label, key in fields:
            tk.Label(self, text=label).pack(pady=(10, 0))
            entry = tk.Entry(self, show="*" if key == "password" else None)
            entry.pack()
            self.entries[key] = entry

        tk.Button(self, text="Aceptar", command=self.register).pack(pady=15)
        tk.Button(self, text="Cancelar", command=self.cancel).pack()

        self.bind("<Escape>", lambda e: self.cancel())

    def register(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}

        if any(not v for v in data.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        ok = create_user(
            data["username"],
            data["name"],
            data["surname"],
            data["password"]
        )

        if not ok:
            messagebox.showerror("Error", "El usuario ya existe")
            return

        messagebox.showinfo("Correcto", "Usuario creado correctamente")
        self.close_and_return()

    def cancel(self):
        self.close_and_return()

    def close_and_return(self):
        self.destroy()
        self.login_window.deiconify()
