import tkinter as tk
from tkinter import ttk


def apply_theme(root: tk.Tk | tk.Toplevel, theme: str):
    """Aplica una paleta de colores simple (light/dark) al `root` y configura estilos ttk.

    Esta función se diseñó para centralizar la lógica de tema y mantener `main_window`
    más limpio. Intenta aplicar cambios por defecto; si algún widget no hereda, se
    puede ajustar desde su propio módulo.
    """
    style = ttk.Style()
    t = (theme or "light").lower()
    if t == "dark":
        bg = "#222327"        # window background
        panel = "#2f3136"     # panels / frames
        fieldbg = "#202225"   # entry / tree bg
        fg = "#e6e6e6"        # text
        heading_bg = "#3b3f45"
        accent = "#4b9bd6"
    else:
        bg = "#f7f7f7"
        panel = "#ededed"
        fieldbg = "#ffffff"
        fg = "#000000"
        heading_bg = "#e6e6e6"
        accent = "#2b7bbf"

    # set base window/bg colors
    try:
        root.configure(bg=bg)
        root.option_add("*Toplevel.background", bg)
        root.option_add("*Background", bg)
        root.option_add("*Foreground", fg)
    except Exception:
        pass

    try:
        style.theme_use("clam")

        style.configure("TFrame", background=panel)
        style.configure("TLabel", background=panel, foreground=fg)

        style.configure("TButton", background=panel, foreground=fg, bordercolor=heading_bg)
        style.map("TButton",
                  background=[("active", heading_bg), ("!disabled", panel)],
                  foreground=[("disabled", "#777777")])

        style.configure("TEntry", fieldbackground=fieldbg, background=fieldbg, foreground=fg)
        style.configure("TCombobox", fieldbackground=fieldbg, background=fieldbg, foreground=fg)
        style.map("TCombobox", fieldbackground=[("readonly", fieldbg)])

        style.configure("Treeview", background=fieldbg, fieldbackground=fieldbg, foreground=fg, bordercolor=heading_bg)
        style.configure("Treeview.Heading", background=heading_bg, foreground=fg)

        style.configure("TCheckbutton", background=panel, foreground=fg)
        style.configure("TRadiobutton", background=panel, foreground=fg)

        try:
            root.option_add("*Menu.background", panel)
            root.option_add("*Menu.foreground", fg)
            root.option_add("*Menu.activeBackground", heading_bg)
        except Exception:
            pass

        style.map('Treeview', background=[('selected', accent)], foreground=[('selected', '#ffffff')])

    except Exception:
        pass


def available_themes():
    return ["light", "dark"]
