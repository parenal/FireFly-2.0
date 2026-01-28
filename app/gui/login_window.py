import tkinter as tk
from tkinter import messagebox
from app.services.auth import authenticate_user
from app.gui.register_window import RegisterWindow


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_login_success=None):
        super().__init__(parent)
        self.parent = parent
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
        tk.Button(self, text="Cancelar", command=self.on_cancel).pack()

        # Recordarme checkbox
        self.remember_var = tk.BooleanVar(value=False)
        tk.Checkbutton(self, text="Recordarme", variable=self.remember_var).pack(pady=(6, 0))

        tk.Button(
            self,
            text="Registrarse",
            command=self.open_register,
            fg="blue"
        ).pack(pady=10)

        self.bind("<Return>", lambda e: self.login())
        self.bind("<Escape>", lambda e: self.on_cancel())

        self.protocol("WM_DELETE_WINDOW", self.on_cancel)
        try:
            parent_mapped = parent.winfo_ismapped()
        except Exception:
            parent_mapped = False

        # Only set transient if parent is visible; if parent is hidden (withdraw),
        # transient to it may prevent the Toplevel from showing on some platforms.
        if parent_mapped:
            try:
                self.transient(parent)
            except Exception:
                pass

        # Ensure the window is visible and on top
        self.deiconify()
        self.lift()
        self.grab_set()
        self.focus_force()
        self.username_entry.focus_set()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = authenticate_user(username, password)

        if not user:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return

        remember = False
        try:
            remember = bool(self.remember_var.get())
        except Exception:
            remember = False

        self.grab_release()
        self.destroy()
        if self.on_login_success:
            # call with remember flag (backwards-compatible)
            try:
                self.on_login_success(user, remember=remember)
            except TypeError:
                # older handlers may accept only user
                self.on_login_success(user)

    def on_cancel(self):
        self.grab_release()
        self.destroy()

    def open_register(self):
        self.withdraw()
        RegisterWindow(self)
