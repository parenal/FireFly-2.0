import tkinter as tk
from tkinter import messagebox
from app.services.auth_service import authenticate_user
from app.gui.register_window import RegisterWindow


class LoginWindow(tk.Tk):
    def __init__(self, on_login_success):
        super().__init__()

        self.on_login_success = on_login_success

        self.title("Inicio de sesión")
        self.geometry("300x220")
        self.resizable(False, False)

        tk.Label(self, text="Usuario").pack(pady=(15, 0))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Contraseña").pack(pady=(10, 0))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Aceptar", command=self.login).pack(pady=10)
        tk.Button(self, text="Cancelar", command=self.destroy).pack()

        tk.Button(
            self,
            text="Registrarse",
            command=self.open_register,
            fg="blue"
        ).pack(pady=10)

        self.bind("<Return>", lambda e: self.login())
        self.bind("<Escape>", lambda e: self.destroy())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = authenticate_user(username, password)

        if not user:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return

        self.destroy()
        self.on_login_success(user)

    def open_register(self):
        self.withdraw()
        RegisterWindow(self)
