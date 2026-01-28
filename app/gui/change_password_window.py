import tkinter as tk
from tkinter import ttk, messagebox
from app.state.session import get_current_user
from app.services.auth import change_password


class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Cambiar contraseña")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        container = ttk.Frame(self, padding=12)
        container.grid(row=0, column=0, sticky="nsew")

        ttk.Label(container, text="Contraseña actual").grid(row=0, column=0, sticky="w")
        self.current_entry = ttk.Entry(container, show="*")
        self.current_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(container, text="Nueva contraseña").grid(row=2, column=0, sticky="w")
        self.new_entry = ttk.Entry(container, show="*")
        self.new_entry.grid(row=3, column=0, sticky="ew", pady=(0, 8))

        ttk.Label(container, text="Repetir nueva contraseña").grid(row=4, column=0, sticky="w")
        self.confirm_entry = ttk.Entry(container, show="*")
        self.confirm_entry.grid(row=5, column=0, sticky="ew", pady=(0, 12))

        buttons = ttk.Frame(container)
        buttons.grid(row=6, column=0, sticky="e")

        ttk.Button(buttons, text="Cancelar", command=self.destroy).grid(row=0, column=0, padx=5)
        ttk.Button(buttons, text="Guardar", command=self.save).grid(row=0, column=1)

        container.columnconfigure(0, weight=1)

        self.bind("<Return>", lambda e: self.save())
        self.bind("<Escape>", lambda e: self.destroy())

        self._fix_window_size(parent)

    def _fix_window_size(self, parent):
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        x = parent.winfo_rootx() + parent.winfo_width() // 2 - w // 2
        y = parent.winfo_rooty() + parent.winfo_height() // 2 - h // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def save(self):
        current = self.current_entry.get().strip()
        new = self.new_entry.get().strip()
        confirm = self.confirm_entry.get().strip()

        if not current or not new or not confirm:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if new != confirm:
            messagebox.showerror("Error", "Las nuevas contraseñas no coinciden")
            return

        user = get_current_user()
        if not user:
            messagebox.showerror("Error", "No hay usuario autenticado")
            return

        try:
            ok = change_password(user.id, current, new)
        except ValueError as e:
            if str(e) == "password_too_long":
                messagebox.showerror("Error", "La nueva contraseña es demasiado larga (máx. 72 bytes). Usa una contraseña más corta.")
                return
            raise

        if not ok:
            messagebox.showerror("Error", "Contraseña actual incorrecta")
            return

        messagebox.showinfo("Correcto", "Contraseña cambiada correctamente")
        self.destroy()
