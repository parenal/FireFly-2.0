import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging
from app.gui.transactions_view import TransactionsView
from app.gui.theme import apply_theme
from app.gui.change_password_window import ChangePasswordWindow


class MainWindow:
    def __init__(self, root, on_logout=None):
        self.root = root
        self.on_logout = on_logout
        root.title("FireFly 2.0 - Control de gastos")
        root.geometry("800x500")

        # Menu de cuenta (cerrar sesión + tema + export)
        from app.gui.export_handlers import create_export_menu
        menubar = tk.Menu(root)
        account_menu = tk.Menu(menubar, tearoff=0)
        account_menu.add_command(label="Cambiar contraseña", command=self._on_change_password)
        account_menu.add_separator()

        # Theme submenu: radiobuttons for light/dark
        try:
            from app.state.session import load_theme, save_theme
            self._theme_var = tk.StringVar(value=load_theme())
        except Exception:
            self._theme_var = tk.StringVar(value="light")

        def _set_theme_to(value):
            try:
                self._theme_var.set(value)
                apply_theme(self.root, value)
                try:
                    save_theme(value)
                except Exception:
                    pass
            except Exception:
                pass

        account_menu.add_radiobutton(label="Tema: Claro", variable=self._theme_var, value="light",
                                     command=lambda: _set_theme_to("light"))
        account_menu.add_radiobutton(label="Tema: Oscuro", variable=self._theme_var, value="dark",
                                     command=lambda: _set_theme_to("dark"))
        account_menu.add_separator()
        account_menu.add_command(label="Cerrar sesión", command=self._on_logout)
        menubar.add_cascade(label="Cuenta", menu=account_menu)
        
        # Export menu
        export_menu = tk.Menu(menubar, tearoff=0)

        def _export_category_chart():
            try:
                dr = self._ask_date_range()
                if dr is None:
                    return
                start_date, end_date = dr
                # ensure dialogs appear on top in Windows
                logger = logging.getLogger('firefly.gui.main_window')
                logger.debug('category - range received %s %s', start_date, end_date)
                try:
                    self.root.attributes('-topmost', True)
                except Exception:
                    pass
                try:
                    path = filedialog.asksaveasfilename(parent=self.root, defaultextension='.png', filetypes=[('PNG Image','*.png')], title='Guardar gráfico por categoría')
                    logger.debug('category - asksaveasfilename returned %r', path)
                    if not path:
                        # try again without parent in case parent causes focus issues
                        logger.debug('retrying asksaveasfilename without parent')
                        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Image','*.png')], title='Guardar gráfico por categoría')
                        logger.debug('category - retry returned %r', path)
                finally:
                    try:
                        self.root.attributes('-topmost', False)
                    except Exception:
                        pass
                if not path:
                    return
                from app.utils.exporter import export_category_chart
                export_category_chart(path, start_date=start_date, end_date=end_date)
                messagebox.showinfo('Exportar', f'Gráfico guardado en: {path}')
            except Exception as e:
                logger = logging.getLogger('firefly.gui.main_window')
                logger.exception('Error exporting category chart')
                messagebox.showerror('Error', f'No se pudo exportar: {e}')

        def _export_monthly_chart():
            try:
                dr = self._ask_date_range()
                if dr is None:
                    return
                start_date, end_date = dr
                logger = logging.getLogger('firefly.gui.main_window')
                logger.debug('monthly - range received %s %s', start_date, end_date)
                try:
                    self.root.attributes('-topmost', True)
                except Exception:
                    pass
                try:
                    path = filedialog.asksaveasfilename(parent=self.root, defaultextension='.png', filetypes=[('PNG Image','*.png')], title='Guardar gráfico mensual')
                    logger.debug('monthly - asksaveasfilename returned %r', path)
                    if not path:
                        logger.debug('retrying monthly asksaveasfilename without parent')
                        path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=[('PNG Image','*.png')], title='Guardar gráfico mensual')
                        logger.debug('monthly - retry returned %r', path)
                finally:
                    try:
                        self.root.attributes('-topmost', False)
                    except Exception:
                        pass

                if not path:
                    messagebox.showwarning('Exportar', 'No se seleccionó fichero para guardar (mensual).')
                    return

                from app.utils.exporter import export_monthly_chart
                export_monthly_chart(path, start_date=start_date, end_date=end_date)
                messagebox.showinfo('Exportar', f'Gráfico guardado en: {path}')
            except Exception as e:
                import traceback
                print(traceback.format_exc())
                messagebox.showerror('Error', f'No se pudo exportar: {e}')

        def _export_excel():
            try:
                logger = logging.getLogger('firefly.gui.main_window')
                logger.debug('_export_excel called')
                dr = self._ask_date_range()
                if dr is None:
                    logger.debug('_export_excel - date range dialog returned None')
                    if messagebox.askyesno('Rango no seleccionado', 'No se seleccionó rango de fechas. ¿Reintentar?'):
                        logger.debug('retrying date-range dialog')
                        dr = self._ask_date_range()
                        if dr is None:
                            logger.debug('_export_excel - retry also returned None')
                            messagebox.showinfo('Exportar', 'Exportación cancelada (no se seleccionó rango).')
                            return
                    else:
                        return
                start_date, end_date = dr
                logger.debug('_export_excel - got range %s %s', start_date, end_date)
                try:
                    self.root.attributes('-topmost', True)
                except Exception:
                    pass

                # attempt to open save dialog; ensure topmost is cleared in finally
                path = None
                try:
                    logger.debug('excel - range received %s %s', start_date, end_date)
                    path = filedialog.asksaveasfilename(parent=self.root, defaultextension='.xlsx', filetypes=[('Excel Workbook','*.xlsx')], title='Guardar transacciones')
                    logger.debug('excel - asksaveasfilename returned %r', path)
                    if not path:
                        logger.debug('retrying excel asksaveasfilename without parent')
                        path = filedialog.asksaveasfilename(defaultextension='.xlsx', filetypes=[('Excel Workbook','*.xlsx')], title='Guardar transacciones')
                        logger.debug('excel - retry returned %r', path)
                except Exception:
                    # if something goes wrong with dialogs, ensure we still clear topmost
                    logger.exception('excel - dialog error')
                finally:
                    try:
                        self.root.attributes('-topmost', False)
                    except Exception:
                        pass

                if not path:
                    messagebox.showwarning('Exportar', 'No se seleccionó ningún fichero para guardar.')
                    return

                from app.utils.exporter import export_transactions_excel
                try:
                    messagebox.showinfo('Exportar', f'Exportando rango: {start_date} → {end_date}')
                except Exception:
                    pass
                logger.debug('calling export_transactions_excel with path %s', path)
                saved = export_transactions_excel(path, start_date=start_date, end_date=end_date)
                logger.debug('export_transactions_excel returned %r', saved)
                messagebox.showinfo('Exportar', f'Archivo guardado en: {saved}')
            except Exception as e:
                logger = logging.getLogger('firefly.gui.main_window')
                logger.exception('Error exporting excel')
                messagebox.showerror('Error', f'No se pudo exportar: {e}')
        export_menu.add_command(label='Gráfico: Gastos por categoría', command=_export_category_chart)
        export_menu.add_command(label='Gráfico: Evolución mensual', command=_export_monthly_chart)
        export_menu.add_separator()
        export_menu.add_command(label='Exportar a Excel (transacciones)', command=_export_excel)
        menubar.add_cascade(label='Exportar', menu=export_menu)
        # attach menu to root
        root.config(menu=menubar)

        style = ttk.Style()
        style.theme_use("clam")

        # apply initial theme from session
        try:
            cur_theme = self._theme_var.get()
        except Exception:
            cur_theme = "light"
        apply_theme(self.root, cur_theme)

        self.app = TransactionsView(root)
        self.app.pack(fill="both", expand=True)

        # Barra de estado inferior con identificador de usuario
        try:
            # store status frame so it can be destroyed on close
            if hasattr(self, "status_frame") and self.status_frame:
                try:
                    self.status_frame.destroy()
                except Exception:
                    pass
            self.status_frame = ttk.Frame(root)
            self.status_frame.pack(side="bottom", fill="x")
            self.user_label = ttk.Label(self.status_frame, text="")
            self.user_label.pack(side="right", padx=8, pady=4)
            self.refresh_user_label()
        except Exception:
            # fallback: create label on root if status frame fails
            try:
                self.user_label = ttk.Label(root, text="")
                self.user_label.place(relx=1.0, x=-10, y=6, anchor="ne")
                self.refresh_user_label()
            except Exception:
                pass

    def _ask_date_range(self):
        # modal dialog to choose start/end dates
        try:
            from tkcalendar import DateEntry
        except Exception:
            messagebox.showerror('Error', 'tkcalendar no disponible')
            return None

        logging.getLogger('firefly.gui.main_window').debug('opening date-range dialog')
        dlg = tk.Toplevel(self.root)
        dlg.title('Rango de fechas')
        dlg.resizable(False, False)
        dlg.transient(self.root)
        dlg.grab_set()

        frm = ttk.Frame(dlg, padding=12)
        frm.pack(fill='both', expand=True)

        ttk.Label(frm, text='Fecha inicio').grid(row=0, column=0, sticky='w')
        start_entry = DateEntry(frm, date_pattern='yyyy-mm-dd')
        start_entry.grid(row=1, column=0, sticky='ew', pady=(0,8))

        ttk.Label(frm, text='Fecha fin').grid(row=2, column=0, sticky='w')
        end_entry = DateEntry(frm, date_pattern='yyyy-mm-dd')
        end_entry.grid(row=3, column=0, sticky='ew', pady=(0,8))

        result = {'ok': False}

        def _on_ok():
            logging.getLogger('firefly.gui.main_window').debug('date-range dialog - OK button pressed')
            try:
                sd = start_entry.get_date()
                ed = end_entry.get_date()
                try:
                    result['start'] = sd.isoformat()
                    result['end'] = ed.isoformat()
                except Exception:
                    result['start'] = sd
                    result['end'] = ed
                result['ok'] = True
            except Exception:
                logging.getLogger('firefly.gui.main_window').exception('date-range dialog - failed to read dates on OK')
            dlg.destroy()

        def _on_cancel():
            logging.getLogger('firefly.gui.main_window').debug('date-range dialog - Cancel pressed')
            dlg.destroy()

        btns = ttk.Frame(frm)
        btns.grid(row=4, column=0, sticky='e')
        ttk.Button(btns, text='Cancelar', command=_on_cancel).grid(row=0, column=0, padx=5)
        ttk.Button(btns, text='Aceptar', command=_on_ok).grid(row=0, column=1)

        frm.columnconfigure(0, weight=1)
        # bind Enter to accept and Escape to cancel
        try:
            dlg.bind('<Return>', lambda e: _on_ok())
            dlg.bind('<Escape>', lambda e: _on_cancel())
        except Exception:
            pass
        self.root.wait_window(dlg)

        logging.getLogger('firefly.gui.main_window').debug('date-range dialog closed; result ok=%s', result.get('ok'))
        if result.get('ok'):
            logging.getLogger('firefly.gui.main_window').debug('returning dates from result dict %s %s', result.get('start'), result.get('end'))
            return (result.get('start'), result.get('end'))
        return None

    def refresh_user_label(self):
        try:
            from app.state.session import get_current_user
            user = get_current_user()
            if user:
                try:
                    self.user_label.config(text=f"Usuario: {user.username}")
                except Exception:
                    self.user_label.config(text=str(user.username))
            else:
                self.user_label.config(text="")
        except Exception:
            pass

    def _on_change_password(self):
        try:
            ChangePasswordWindow(self.root)
        except Exception:
            # as a fallback, show an error
            try:
                messagebox.showerror('Error', 'No se pudo abrir la ventana de cambio de contraseña')
            except Exception:
                pass

    def _on_logout(self):
        try:
            if messagebox.askyesno('Cerrar sesión', '¿Seguro que deseas cerrar la sesión?'):
                if callable(self.on_logout):
                    try:
                        self.on_logout()
                    except Exception:
                        pass
        except Exception:
            # ensure we still call the callback if possible
            try:
                if callable(self.on_logout):
                    self.on_logout()
            except Exception:
                pass

    def close(self):
        try:
            try:
                if hasattr(self, 'app') and self.app:
                    try:
                        self.app.destroy()
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                if hasattr(self, 'status_frame') and self.status_frame:
                    try:
                        self.status_frame.destroy()
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                self.root.config(menu=None)
            except Exception:
                pass
        except Exception:
            pass