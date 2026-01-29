# Aplicación de Finanzas Personales

Este proyecto es una aplicación de **finanzas personales** que permite registrar, analizar y visualizar **ingresos y gastos**.  

La aplicación dispone actualmente de **dos modos de uso**:
# FireFly 2.0 — Control de gastos (Finanzas personales)

Aplicación de finanzas personales para registrar, visualizar y exportar ingresos y gastos.

Contenido del README:

- Requisitos e instalación
- Ejecución (GUI y CLI)
- Funcionalidades principales
- Balance mensual/anual y cómo se calcula
- Exportar datos y gráficos
- Desarrollo y pruebas
- Variables de entorno y seguridad
- Solución de problemas comunes

---

## Requisitos

- Python 3.10 o superior
- Virtualenv recomendado
- Dependencias en `requirements.txt`

Instalación rápida:

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
```

---

## Ejecución

GUI (interfaz gráfica):

```bash
python run_gui.py
```

CLI (línea de comandos):

```bash
python -m app.main <comando> [opciones]
```

---

## Funcionalidades principales

- Registrar transacciones (ingresos y gastos) desde GUI o CLI.
- Visualizar lista de transacciones filtradas por mes/año.
- Panel de balances: muestra Ingresos, Gastos y Balance neto del mes seleccionado.
- Gráficos:
	- Gastos por categoría (PNG)
	- Evolución mensual de ingresos/gastos (PNG)
- Exportar transacciones a Excel/CSV.
- Gestión de sesión y cambio de contraseña desde la GUI.

---

## Balance: cómo se calcula

- Las transacciones tienen un `type` (`income` o `expense`) y un `amount` numérico.
- Internamente los gastos pueden almacenarse con signo negativo; las pantallas y los cálculos muestran los gastos como valores absolutos (sumamos |amount| para gastos).
- Netos:
	- Ingresos = suma de importes con `type == 'income'`
	- Gastos = suma absoluta de importes con `type == 'expense'`
	- Balance = Ingresos − Gastos

En la GUI el panel de balances se actualiza al cambiar Mes/Año y después de añadir/editar/eliminar transacciones.

---

## Exportar datos y gráficos

- Desde el menú `Exportar` puedes generar:
	- Gráfico de gastos por categoría (PNG)
	- Gráfico de evolución mensual (PNG)
	- Exportar transacciones a Excel (`.xlsx`) o CSV (fallback si `openpyxl` no está instalado)

- Para evitar que los diálogos de archivo se queden detrás de la ventana en Windows, la app intenta mostrar el diálogo con la ventana como `parent` y reintenta sin `parent` si hay problemas de foco.

---

## Desarrollo y pruebas

- Estructura principal del proyecto:

```
app/
	gui/                # ventanas y vistas (Tkinter)
	services/           # lógica de negocio (transacciones, reports, auth)
	models/             # modelos SQLAlchemy
	state/              # sesión y preferencias
	utils/              # helpers (exporter, etc.)
run_gui.py
requirements.txt
README.md
```

- Desarrollo:
	- La carpeta `app/` contiene las piezas principales: GUI, servicios, modelos y estado.
	- Para añadir funcionalidades, crea módulos en `app/services` y ventanas en `app/gui`.
	- Mantén `requirements.txt` actualizado cuando añadas dependencias.

---

## Variables de entorno y seguridad

- La aplicación usa cifrado (Fernet) para datos sensibles. Define la clave en la variable de entorno `FIREFLY_FERNET_KEY` antes de ejecutar la app en entornos de producción.

Ejemplo (Windows PowerShell):

```powershell
$env:FIREFLY_FERNET_KEY = 'tu_clave_base64'
python run_gui.py
```

Notas de seguridad:

- No incluyas la clave en el repositorio.
- Realiza backups periódicos de `data/*.db` y almacénalos cifrados si contienen datos sensibles.

---

## Problemas comunes

- Ventana en blanco al iniciar: asegúrate de que no haya errores en consola; `run_gui.py` configura logging para ver mensajes de depuración.
- Diálogo de selección de archivo detrás de la ventana en Windows: la app reintenta sin `parent` si detecta problemas.
- Export a Excel falla por `openpyxl` ausente: la app guarda en CSV como fallback.

Si encuentras errores, ejecuta `python run_gui.py` desde una terminal para ver trazas y reportarlas.

---

## Contribuir

- Crea un fork, trabaja en una rama y abre PR con cambios claros.
- Añade pruebas para nuevas funcionalidades.
- Mantén `requirements.txt` actualizado con versiones fijas.

---

Si quieres, puedo:

- Añadir instrucciones para empaquetar la aplicación (PyInstaller/briefcase).
- Añadir ejemplos de fichero de configuración o `.env`.
- Generar un changelog básico con los cambios que hemos aplicado.

— Fin —

---

## Empaquetado — Generar ejecutable (Windows)

Se incluye un script de ejemplo para Windows en `scripts/build_windows_exe.ps1` que usa `PyInstaller`.

Pasos rápidos (Windows, con venv activado):

```powershell
pip install pyinstaller
./scripts/build_windows_exe.ps1 -Name FireFly -Entry run_gui.py -NoConsole
```

Notas y recomendaciones:
- El script añade la carpeta `data` junto al ejecutable (`--add-data "data;data"`). Si necesitas incluir otros ficheros o recursos, añade más `--add-data` al comando.
- Si la app usa paquetes con datos adicionales (por ejemplo `tkcalendar`), PyInstaller debería detectarlos; si algo falta, añade hooks o especifica `--hidden-import`.
- Resultado: `dist\FireFly.exe` (o similar). Copia la carpeta `data` si no la has incluido en el binario.

Si quieres, puedo:
- Probar y ajustar el comando `pyinstaller` para incluir icono, assets y otros recursos.
- Añadir un `build.bat` para usuarios que prefieran doble clic en Windows.

