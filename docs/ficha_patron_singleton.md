# Ficha de patrón: Singleton

| Campo | Descripción |
|---|---|
| **Patrón y tipo** | Singleton – Creacional |
| **Problema que resuelve en NUESTRO proyecto** | El sistema necesita acceder a la base de datos SQLite desde diferentes partes de la aplicación. Crear y administrar varias instancias de la clase de acceso a datos puede generar conexiones innecesarias y dificultar el control del acceso a la base de datos. |
| **Dónde está en el código** | Archivo `main.py`, clase `Database`. La implementación utiliza el atributo `_instance` y el método especial `__new__(cls)` para reutilizar la misma instancia. `SistemaPOS` obtiene la instancia mediante `Database()`. |
| **Cómo funciona (3 líneas)** | La clase `Database` almacena la instancia creada en el atributo `_instance`. Cuando se solicita nuevamente `Database()`, el método `__new__()` devuelve la instancia existente en lugar de crear otra. Así se reutiliza el mismo objeto de acceso a la base de datos durante la ejecución del programa. |
| **Antes y después** | **Antes:** crear instancias independientes para acceder a los datos podría complicar la administración de la conexión. **Después:** las llamadas a `Database()` reutilizan la misma instancia, centralizando el acceso a SQLite. |
| **Diagrama de clases (simple)** | `SistemaPOS` → `Database` → `SQLite`. `Database` contiene `_instance` y `connection`; su método `__new__(cls)` controla la creación de la instancia y esta administra la conexión con `pos_veterinaria.db`. |
| **Cómo lo probamos** | Ejecutar `db1 = Database()` y `db2 = Database()` en el mismo programa. Comprobar `print(db1 is db2)` y `print(db1.connection is db2.connection)`. El resultado esperado de ambas expresiones es `True`; se debe ejecutar la prueba para confirmar los resultados. |
| **Qué mejoraríamos** | Agregar un mecanismo para cerrar la conexión al finalizar el programa y revisar la sincronización de la instancia si en el futuro se utilizan varios hilos de ejecución. |
