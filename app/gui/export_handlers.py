import tkinter as tk
from tkinter import messagebox, filedialog
import traceback

from app.utils import exporter as _exporter


def create_export_menu(parent_window):
    """Create and return an Export menu bound to the given MainWindow-like object.

    parent_window must expose:
      - root: the Tk root or Toplevel
      - _ask_date_range(): method that returns (start, end) or None
    """
    menu = tk.Menu(parent_window.root, tearoff=0)

    def _export_category_chart():
        try:
            dr = parent_window._ask_date_range()
            if not dr:
                return
            start_date, end_date = dr
            path = filedialog.asksaveasfilename(parent=parent_window.root,
                                                defaultextension='.png',
                                                filetypes=[('PNG Image', '*.png')],
                                                title='Guardar gráfico por categoría')
            if not path:
                return
            _exporter.export_category_chart(path, start_date=start_date, end_date=end_date)
            messagebox.showinfo('Exportar', f'Gráfico guardado en: {path}')
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror('Error', f'No se pudo exportar: {e}')

    def _export_monthly_chart():
        try:
            dr = parent_window._ask_date_range()
            if not dr:
                return
            start_date, end_date = dr
            path = filedialog.asksaveasfilename(parent=parent_window.root,
                                                defaultextension='.png',
                                                filetypes=[('PNG Image', '*.png')],
                                                title='Guardar gráfico mensual')
            if not path:
                return
            _exporter.export_monthly_chart(path, start_date=start_date, end_date=end_date)
            messagebox.showinfo('Exportar', f'Gráfico guardado en: {path}')
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror('Error', f'No se pudo exportar: {e}')

    def _export_transactions_excel():
        try:
            dr = parent_window._ask_date_range()
            if not dr:
                return
            start_date, end_date = dr
            path = filedialog.asksaveasfilename(parent=parent_window.root,
                                                defaultextension='.xlsx',
                                                filetypes=[('Excel Workbook', '*.xlsx')],
                                                title='Guardar transacciones')
            if not path:
                return
            saved = _exporter.export_transactions_excel(path, start_date=start_date, end_date=end_date)
            messagebox.showinfo('Exportar', f'Archivo guardado en: {saved}')
        except Exception as e:
            print(traceback.format_exc())
            messagebox.showerror('Error', f'No se pudo exportar: {e}')

    menu.add_command(label='Gráfico: Gastos por categoría', command=_export_category_chart)
    menu.add_command(label='Gráfico: Evolución mensual', command=_export_monthly_chart)
    menu.add_separator()
    menu.add_command(label='Exportar a Excel (transacciones)', command=_export_transactions_excel)

    return menu
