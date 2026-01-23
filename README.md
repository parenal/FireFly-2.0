# Aplicación de Finanzas Personales

Este proyecto es una aplicación de **finanzas personales** que permite registrar, analizar y visualizar **ingresos y gastos**.  

La aplicación dispone actualmente de **dos modos de uso**:

* **Interfaz de línea de comandos (CLI)** – completamente funcional  
* **Interfaz gráfica (GUI)** – disponible y en evolución

Ambas interfaces utilizan el mismo backend y los mismos datos, por lo que son totalmente compatibles entre sí.

---

## Requisitos

* Python 3.10 o superior  
* Dependencias instaladas (según `requirements.txt`)

Instalación de dependencias:

```bash
pip install -r requirements.txt
```

---

## Modos de ejecución

### Ejecución por línea de comandos (CLI)

```bash
python -m app.main <comando> [opciones]
```

### Ejecución de la interfaz gráfica (GUI)

```bash
python run_gui.py
```

---

## Interfaz Gráfica (GUI)

La aplicación cuenta con una **interfaz gráfica de usuario** que permite realizar las principales operaciones sin necesidad de usar la terminal.

Para iniciarla:

```bash
python run_gui.py
```

Funcionalidades disponibles desde la GUI:

* Añadir ingresos y gastos
* Visualizar gráficos de gastos por categoría
* Visualizar evolución mensual de ingresos y gastos
* Consultar el balance general
* Revisar transacciones registradas

> La GUI se encuentra en desarrollo activo y se irá ampliando progresivamente con nuevas funcionalidades y mejoras visuales.

---

## Interfaz de Línea de Comandos (CLI)

A continuación se detallan **todos los comandos actualmente soportados** en modo CLI.

---

### 1. Mostrar gráfico de gastos por categoría

Genera un gráfico de barras con el total de gastos agrupados por categoría.

```bash
python -m app.main graph-category
```

Uso típico:

* Analizar en qué categorías se gasta más dinero

---

### 2. Mostrar gráfico de evolución mensual

Genera un gráfico de líneas con la evolución mensual de **ingresos** y **gastos**.

```bash
python -m app.main graph-monthly
```

Uso típico:

* Comparar ingresos vs gastos mes a mes  
* Detectar tendencias de ahorro o sobrecoste

---

### 3. Añadir un gasto

Registra una nueva transacción de tipo **gasto**.

```bash
python -m app.main add --t-type expense --amount <cantidad> --category <categoria>
```

Ejemplo:

```bash
python -m app.main add --t-type expense --amount 10 --category COMIDA
```

Notas:

* `amount` debe ser un valor numérico (se permiten decimales)
* `category` es libre y definida por el usuario

---

### 4. Añadir un ingreso

Registra una nueva transacción de tipo **ingreso**.

```bash
python -m app.main add --t-type income --amount <cantidad> --category <categoria>
```

Ejemplo:

```bash
python -m app.main add --t-type income --amount 1500 --category salario
```

Notas:

* `amount` y `category` son variables
* La categoría puede representar cualquier concepto (salario, extra, devolución, etc.)

---

### 5. Ver balance general

Muestra en terminal el balance total acumulado:

* Total de ingresos  
* Total de gastos  
* Balance final  

```bash
python -m app.main balance
```

Uso típico:

* Consultar rápidamente la situación financiera actual

---

### 6. Listar últimas transacciones

Muestra en terminal una lista de las transacciones más recientes.

```bash
python -m app.main list
```

Uso típico:

* Revisar movimientos recientes  
* Verificar que una transacción se ha registrado correctamente

---

## Estado del proyecto

* ✅ Backend funcional  
* ✅ Persistencia de transacciones  
* ✅ Visualización mediante gráficos (Matplotlib)  
* ✅ Interfaz CLI completa  
* 🚧 Interfaz gráfica en desarrollo continuo  

---

## Notas finales

Este proyecto está diseñado para ser utilizado tanto por usuarios que prefieren **terminal** como por aquellos que optan por una **interfaz gráfica** más visual.  

El README se irá actualizando conforme se añadan nuevos comandos, opciones avanzadas y mejoras en la GUI.
