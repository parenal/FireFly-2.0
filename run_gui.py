import tkinter as tk
import logging
from app.gui.login_window import LoginWindow
from app.gui.main_window import MainWindow
from app.state.session import set_current_user
import sys
import traceback


def main():
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    log = logging.getLogger("firefly")
    log.debug("Creando root Tk")
    root = tk.Tk()
    log.debug("Ocultando root")
    root.withdraw()  # ocultamos root al inicio

    main_win = {"instance": None}

    def on_login_success(user, remember=False):
        set_current_user(user)
        root.deiconify()        # mostramos ventana principal

        def logout_action():
            from app.state.session import clear_current_user
            # close current main window UI
            try:
                if main_win["instance"]:
                    main_win["instance"].close()
            except Exception:
                pass

            clear_current_user()
            root.withdraw()
            # show login window again
            LoginWindow(root, on_login_success=on_login_success)

        # create main window and keep reference
        main_win["instance"] = MainWindow(root, on_logout=logout_action)
        # manage remember me
        try:
            from app.state.session import remember_user, clear_remembered_user
            if remember:
                remember_user(user.username)
            else:
                clear_remembered_user()
        except Exception:
            pass

    log.debug("Lanzando LoginWindow")
    # Auto-login si hay usuario recordado
    try:
        from app.state.session import get_remembered_username
        from app.services.auth import get_user_by_username

        remembered = get_remembered_username()
        if remembered:
            user = get_user_by_username(remembered)
            if user:
                print("[debug] Auto-login usuario recordado:", remembered)
                on_login_success(user, remember=True)
            else:
                LoginWindow(root, on_login_success=on_login_success)
        else:
            LoginWindow(root, on_login_success=on_login_success)
    except Exception:
        LoginWindow(root, on_login_success=on_login_success)
    log.debug("Entrando en mainloop")
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception('Unhandled exception in main')
        try:
            input("Ha ocurrido un error. Pulsa Enter para salir...")
        except Exception:
            pass
        sys.exit(1)
