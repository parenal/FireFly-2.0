# 🔥 FireFly 2.0 — Finanzas Personales

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat)

Aplicación de finanzas personales para registrar, analizar y visualizar ingresos y gastos. Disponible como interfaz gráfica (GUI) y línea de comandos (CLI).

---

## ✨ Características

- 📊 **Dashboard de balances** — ingresos, gastos y balance neto por mes/año
- 📈 **Gráficos** — gastos por categoría y evolución mensual (exportables a PNG)
- 📤 **Exportación** — Excel (`.xlsx`) y CSV
- 🔒 **Seguridad** — cifrado Fernet para datos sensibles, gestión de sesión con contraseña
- 🖥️ **Doble interfaz** — GUI con Tkinter y CLI con Typer
- 📦 **Empaquetable** — genera ejecutable `.exe` para Windows con PyInstaller

---

## 🛠️ Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.10+ |
| GUI | Tkinter + tkcalendar |
| CLI | Typer + Rich |
| Base de datos | SQLite + SQLAlchemy 2.0 |
| Gráficos | Matplotlib + NumPy |
| Exportación | Pandas + openpyxl |
| Seguridad | Cryptography (Fernet) + argon2 |
| Empaquetado | PyInstaller |

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/parenal/FireFly-2.0.git
cd FireFly-2.0

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\Activate.ps1  # Windows PowerShell

# Instalar dependencias
pip install -r requirements.txt
```

---

## ▶️ Uso

**Interfaz gráfica:**
```bash
python run_gui.py
```

**Línea de comandos:**
```bash
python -m app.main --help
```

---

## 📁 Estructura del proyecto

```
FireFly-2.0/
├── app/
│   ├── gui/          # Ventanas y vistas (Tkinter)
│   ├── services/     # Lógica de negocio
│   ├── models/       # Modelos SQLAlchemy
│   ├── state/        # Sesión y preferencias
│   └── utils/        # Exportador, helpers
├── data/             # Base de datos local
├── scripts/          # Script de build para Windows
├── run_gui.py        # Punto de entrada GUI
└── requirements.txt
```

---

## 🔐 Variables de entorno

```bash
# Clave de cifrado Fernet (producción)
export FIREFLY_FERNET_KEY="tu_clave_base64"
```

> ⚠️ Nunca incluyas la clave en el repositorio.

---

## 📦 Generar ejecutable (Windows)

```powershell
pip install pyinstaller
./scripts/build_windows_exe.ps1 -Name FireFly -Entry run_gui.py -NoConsole
# Resultado: dist/FireFly.exe
```

---

## 📄 Licencia

MIT © Pablo Arenal
