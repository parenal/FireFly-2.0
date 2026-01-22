# Aplicación de Finanzas Personales (CLI)

Este proyecto es una aplicación de finanzas personales que actualmente se maneja **mediante línea de comandos (CLI)**. Aunque la interfaz gráfica está en desarrollo, todas las funcionalidades principales ya están disponibles desde terminal.

Este documento describe **los comandos actualmente soportados**, su propósito y ejemplos de uso.

---

## Requisitos

* Python 3.10 o superior
* Dependencias instaladas (según `requirements.txt`)

Ejecución general:

```bash
python -m app.main <comando> [opciones]
```

---

## Comandos disponibles

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
* Detectar tendencias

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

* `amount` es un valor numérico (decimal permitido)
* `category` es libre y depende del usuario

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
* La categoría puede ser cualquier concepto (salario, extra, devolución, etc.)

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
* ✅ Visualización por gráficos (Matplotlib)
* 🚧 Interfaz gráfica en desarrollo

Este README se irá ampliando conforme se incorporen nuevas funcionalidades.
