

# Sistema de Inventario y Ventas - POS (Veterinaria)

Sistema de punto de venta (POS) de escritorio desarrollado en Python utilizando Tkinter para la interfaz gráfica y SQLite (pos_veterinaria.db) como base de datos relacional. El software está diseñado para la gestión integral de un establecimiento veterinario, abarcando el control de inventarios, usuarios, registro de ventas transaccionales y generación de reportes.

---

## Equipo de Desarrollo y Roles

* Nikol – Arquitectura general, interfaz gráfica (Tkinter), integración de módulos y gestión del repositorio.
* Andrey Alirio Pinzón Baltazar – Implementación y documentación del Patrón Estructural (Facade - VentaFacade).


* Yoni Steben Torres Quintero – Implementación y documentación del Patrón Creacional (Singleton - Database).



---

## Patrones de Diseño Implementados

El proyecto aplica rigurosamente principios de diseño de software orientados a objetos y patrones GoF (Gang of Four), reflejados directamente en el código fuente (main.py):

### 1. Patrón Creacional: Singleton (Database)

* Propósito: Garantizar que exista una única instancia de conexión a la base de datos pos_veterinaria.db durante toda la ejecución del programa.


* Implementación: Se gestiona mediante el método especial **new** en la clase Database, centralizando el acceso a los cursores y previniendo bloqueos por múltiples conexiones concurrentes.



### 2. Patrón Estructural: Facade (VentaFacade)

* Propósito: Proveer una interfaz unificada y simplificada para un subsistema complejo de transacciones comerciales.


* Implementación: La clase VentaFacade encapsula toda la lógica crítica al registrar una venta (cálculo de totales, validación de stock disponible, actualización del inventario de productos, registro maestro de la venta y almacenamiento detallado de los ítems), manejando de forma segura las transacciones (commit / rollback) fuera de la interfaz gráfica.



---

## Estructura del Proyecto
```text
Sistema_inventario_ventas_POS/
│
├── main.py                  # Código fuente principal de la aplicación
├── pos_veterinaria.db       # Base de datos SQLite integrada
├── README.md                # Documentación general del repositorio
└── docs/                    # Carpeta de documentación académica (Entregables)
    ├── ficha_patron_facade.md     # Ficha técnica de Andrey (Facade)
    └── ficha_patron_singleton.md  # Ficha técnica de Yoni (Singleton)
```


---
## Requisitos y Ejecución

**1. Requisitos previos:** 
Tener instalado Python (versión 3.x recomendada).

**2. Clonar el repositorio:**
git clone https://github.com/Nikol650-eng/Sistema_inventario_ventas_POS.git

3. Ejecutar la aplicación:
python main.py

### Credenciales de Acceso Inicial

* Usuario: admin


* Contraseña: admin123
