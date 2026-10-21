# Sistema de Inventario y Ventas - POS (Veterinaria)

## 1. Descripción del proyecto

El Sistema de Inventario y Ventas - POS (Veterinaria) es una aplicación de escritorio desarrollada en Python, utilizando Tkinter para la interfaz gráfica y SQLite para el almacenamiento de información.

El sistema está orientado a la gestión de productos, el control del inventario y el registro de ventas. Además, implementa patrones de diseño de software para organizar las responsabilidades y facilitar el mantenimiento del código.

## 2. Integrantes y responsabilidades

| Integrante | Responsabilidades |
|---|---|
| Cielo Nikol Solarte Lopez | Arquitectura general, desarrollo de la interfaz gráfica con Tkinter, integración de módulos y gestión del repositorio. |
| Andrey Alirio Pinzón Baltazar | Implementación y documentación del patrón estructural Facade mediante la clase `VentaFacade`. |
| Yoni Steben Torres Quintero | Implementación y documentación del patrón creacional Singleton mediante la clase `Database`. |

## 3. Funcionalidades principales

El proyecto contempla las siguientes funcionalidades:

- Inicio de sesión.
- Administración y consulta de productos.
- Consulta de existencias disponibles.
- Registro de ventas.
- Selección de productos y cantidades para una venta.
- Validación de existencias durante el proceso de venta.
- Actualización del inventario después de una venta.
- Almacenamiento de información en una base de datos SQLite.
- Consulta de reportes disponibles en la aplicación.

Las funcionalidades descritas corresponden al alcance del sistema y deben verificarse en la versión actual del código antes de la demostración.

## 4. Patrones de diseño implementados

El proyecto integra un patrón creacional y uno estructural.

### 4.1. Singleton — Patrón creacional

**Clase:** `Database`

**Archivo:** `main.py`

La clase `Database` utiliza el método especial `__new__` y el atributo `_instance` para controlar la creación de instancias.

La primera llamada crea la instancia y establece la conexión con la base de datos. Las llamadas posteriores reutilizan la instancia existente.

**Problema que resuelve:** evita crear innecesariamente múltiples instancias de la clase encargada de gestionar el acceso a la base de datos.

### 4.2. Facade — Patrón estructural

**Clase:** `VentaFacade`

**Archivo:** `main.py`

**Método principal:** `registrar_venta()`.

El patrón Facade proporciona una interfaz simplificada para coordinar las operaciones necesarias durante el registro de una venta.

La clase `VentaFacade` centraliza el proceso de venta, incluyendo las validaciones de existencias, el registro de la venta y sus detalles, y la actualización del inventario.

El proceso utiliza `commit()` para confirmar la transacción y `rollback()` para revertirla cuando se produce una excepción durante la operación.

**Problema que resuelve:** reduce la cantidad de lógica de negocio que debe gestionar la interfaz gráfica y centraliza las operaciones relacionadas con el registro de ventas.

## 5. Tecnologías utilizadas

- **Python 3:** lenguaje de programación.
- **Tkinter:** desarrollo de la interfaz gráfica.
- **SQLite:** almacenamiento de información mediante una base de datos local.
- **Git:** control de versiones.
- **GitHub:** alojamiento del repositorio y colaboración del equipo.

El proyecto utiliza módulos de la biblioteca estándar de Python, como `tkinter`, `sqlite3` y `datetime`.

## 6. Requisitos previos

Para ejecutar el proyecto se necesita:

- Tener Python 3 instalado.
- Tener Git instalado para clonar el repositorio.
- Contar con Tkinter disponible en la instalación de Python.
- Disponer del archivo `pos_veterinaria.db`, incluido en el repositorio.

No se requiere instalar paquetes externos para los módulos estándar mencionados.

## 7. Instalación y ejecución

Sigue estos tres pasos para ejecutar la aplicación.

### Paso 1. Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/Nikol650-eng/Sistema_inventario_ventas_POS.git
```

### Paso 2. Ingresar a la carpeta del proyecto

```bash
cd Sistema_inventario_ventas_POS
```

### Paso 3. Ejecutar la aplicación

```bash
python main.py
```

Si tu instalación utiliza el comando `python3`, ejecuta:

```bash
python3 main.py
```

Ejecuta el programa desde la carpeta del proyecto para que pueda localizar el archivo de base de datos `pos_veterinaria.db`.

## 8. Credenciales de acceso

Las credenciales iniciales documentadas para el proyecto son:

- **Usuario:** `admin`
- **Contraseña:** `admin123`

Estas credenciales deben corresponder a la configuración de la base de datos utilizada por la aplicación.

Son credenciales de prueba y no deben utilizarse como configuración segura en un entorno de producción.

## 9. Estructura del proyecto

```text
Sistema_inventario_ventas_POS/
├── docs/
│   ├── ficha_patron_facade.md
│   ├── ficha_patron_singleton.md
│   ├── roles.pdf
│   └── trello.png
├── main.py
├── pos_veterinaria.db
└── README.md
```

### Descripción de los archivos

- `main.py`: contiene la interfaz gráfica, el acceso a la base de datos y las clases relacionadas con los patrones Singleton y Facade.
- `pos_veterinaria.db`: base de datos SQLite del sistema.
- `docs/ficha_patron_facade.md`: documentación del patrón estructural Facade.
- `docs/ficha_patron_singleton.md`: documentación del patrón creacional Singleton.
- `docs/Roles.pdf`: documento con la distribución de roles y responsabilidades del equipo.
- `docs/Trello.png`: captura del tablero de Trello utilizado para organizar y dar seguimiento a las tareas del equipo.
- `README.md`: documentación general e instrucciones de ejecución del proyecto.

## 10. Documentación de los patrones de diseño

Las fichas de los patrones de diseño se encuentran en la carpeta `docs/`:

- [Ficha del patrón Facade](docs/ficha_patron_facade.md)
- [Ficha del patrón Singleton](docs/ficha_patron_singleton.md)

Cada ficha describe el problema que aborda el patrón, su ubicación en el código, la comparación entre la situación anterior y la solución implementada, y un diagrama de clases.

## 11. Organización y seguimiento del equipo

La distribución de responsabilidades se documenta en el archivo `docs/roles.pdf`.

El seguimiento de las actividades del proyecto se realiza mediante un tablero de Trello, cuya captura se encuentra en `docs/trello.png`.

Estos recursos permiten documentar la organización del equipo, la asignación de responsabilidades y el seguimiento de las tareas del proyecto.

## 12. Escenarios para la demostración

Durante la socialización se recomienda comprobar los siguientes escenarios:

1. **Inicio de sesión:** ingresar con las credenciales de prueba.
2. **Consulta del inventario:** revisar los productos y las existencias disponibles.
3. **Registro de una venta válida:** seleccionar productos, definir cantidades y completar la venta.
4. **Actualización del inventario:** verificar que las existencias cambien después de una venta confirmada.
5. **Venta con existencias insuficientes:** verificar que el sistema muestre un error controlado.
6. **Demostración de Singleton:** mostrar cómo las llamadas a `Database()` reutilizan la misma instancia.
7. **Demostración de Facade:** mostrar cómo `VentaFacade.registrar_venta()` coordina las operaciones del proceso de venta.

Antes de la presentación, se deben ejecutar las pruebas para comprobar los resultados. En particular, conviene verificar que una venta fallida no deje cambios parciales en la base de datos.

## 13. Control de versiones y trabajo en equipo

El proyecto utiliza Git y GitHub para administrar el código fuente, conservar el historial de cambios y facilitar la colaboración entre los integrantes.

El historial de commits permite consultar las contribuciones realizadas por los miembros del equipo.

**Repositorio del proyecto:** [Sistema de Inventario y Ventas - POS (Veterinaria)](https://github.com/Nikol650-eng/Sistema_inventario_ventas_POS)

**Historial de commits:** [Consultar los cambios del proyecto](https://github.com/Nikol650-eng/Sistema_inventario_ventas_POS/commits/main/)

## 14. Objetivo académico

El objetivo del proyecto es aplicar patrones de diseño de software a un sistema funcional, identificando problemas concretos y utilizando soluciones que favorezcan la organización, el mantenimiento y la comprensión del código.

La implementación de Singleton y Facade permite demostrar la aplicación práctica de un patrón creacional y uno estructural dentro del flujo del sistema POS.

