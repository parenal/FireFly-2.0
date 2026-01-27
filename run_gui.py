import tkinter as tk

from app.gui.login_window import LoginWindow
from app.gui.transactions_view import TransactionsView


def run_app():
    root = tk.Tk()
    root.withdraw()  # OCULTAMOS la ventana raíz al inicio

    def on_login_success(user):
        """
        Se llama cuando el login es correcto
        """
        login_window.destroy()

        main_window = tk.Toplevel(root)
        app = TransactionsView(main_window, user=user)
        main_window.protocol("WM_DELETE_WINDOW", root.quit)
        main_window.mainloop()

    def on_login_cancel():
        """
        Se llama si el usuario cancela el login
        """
        root.quit()

    login_window = tk.Toplevel(root)
    LoginWindow(
        login_window,
        on_success=on_login_success,
        on_cancel=on_login_cancel
    )

    root.mainloop()


if __name__ == "__main__":
    run_app()
