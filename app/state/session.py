"""Módulo simple para gestionar el usuario actual en sesión.

Se mantiene en memoria; suficiente para la ejecución local de la GUI.
"""

import os

_current_user = None

def set_current_user(user):
	"""Establece el usuario actualmente logueado."""
	global _current_user
	_current_user = user

def get_current_user():
	"""Devuelve el usuario actualmente logueado o None."""
	return _current_user

def clear_current_user():
	"""Limpia la sesión actual."""
	global _current_user
	_current_user = None


# ------------------
# Remember me helpers
# ------------------
def _remember_file_path():
	import os
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
	return os.path.join(root, "data", "remembered_user.txt")


def remember_user(username: str):
	"""Persiste el nombre de usuario para 'recordarme'."""
	try:
		path = _remember_file_path()
		dirpath = os.path.dirname(path)
		os.makedirs(dirpath, exist_ok=True)
		with open(path, "w", encoding="utf-8") as f:
			f.write(username)
	except Exception:
		pass


def get_remembered_username():
	"""Devuelve el nombre de usuario guardado o None."""
	try:
		path = _remember_file_path()
		if not os.path.exists(path):
			return None
		with open(path, "r", encoding="utf-8") as f:
			return f.read().strip() or None
	except Exception:
		return None


def clear_remembered_user():
	"""Elimina el usuario recordado."""
	try:
		path = _remember_file_path()
		if os.path.exists(path):
			os.remove(path)
	except Exception:
		pass


# ------------------
# Theme persistence
# ------------------
def _theme_file_path():
	root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
	return os.path.join(root, "data", "theme.cfg")


def save_theme(theme: str):
	"""Guarda el tema seleccionado ('light' o 'dark')."""
	try:
		path = _theme_file_path()
		dirpath = os.path.dirname(path)
		os.makedirs(dirpath, exist_ok=True)
		with open(path, "w", encoding="utf-8") as f:
			f.write(theme)
	except Exception:
		pass


def load_theme() -> str:
	"""Carga el tema persistido. Devuelve 'light' por defecto si no existe."""
	try:
		path = _theme_file_path()
		if not os.path.exists(path):
			return "light"
		with open(path, "r", encoding="utf-8") as f:
			t = f.read().strip().lower()
			return t if t in ("light", "dark") else "light"
	except Exception:
		return "light"
