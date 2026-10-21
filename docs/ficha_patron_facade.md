# Ficha de patrón: Facade (Fachada)

| Campo | Descripción |
|---|---|
| **Patrón y tipo** | Facade (Fachada) – Estructural |
| **Problema que resuelve en NUESTRO proyecto** | Registrar una venta requiere coordinar varias operaciones: calcular el total, validar los productos y sus existencias, guardar la venta y sus detalles, y actualizar el inventario. Si estas operaciones se coordinan directamente desde la interfaz gráfica, aumenta la complejidad del código y se dificulta su mantenimiento. |
| **Dónde está en el código** | Archivo `main.py`, clase `VentaFacade`, método `registrar_venta(usuario, medio_pago, carrito)`. La clase `SistemaPOS` utiliza la fachada mediante `self.venta_facade.registrar_venta(...)`. |
| **Cómo funciona (3 líneas)** | La fachada centraliza el proceso de registro de una venta en un solo método. Coordina las operaciones de venta, validación de existencias y actualización del inventario mediante la base de datos. Si el proceso termina correctamente confirma la transacción con `commit()`; si ocurre una excepción, ejecuta `rollback()`. |
| **Antes y después** | **Antes:** la interfaz gráfica debía coordinar las distintas operaciones necesarias para registrar una venta. **Después:** la interfaz llama a `registrar_venta()` y `VentaFacade` coordina el proceso, reduciendo la complejidad de la interfaz. |
| **Diagrama de clases (simple)** | `SistemaPOS` → `VentaFacade` → `Database` → `SQLite`. `SistemaPOS` utiliza `VentaFacade`; la fachada utiliza `Database`, que administra el acceso a `pos_veterinaria.db`. |
| **Cómo lo probamos** | Registrar una venta con existencias suficientes y verificar el registro y la actualización del inventario. Después, intentar vender una cantidad superior a la disponible y comprobar que se rechace la operación. Registrar los resultados después de ejecutar ambas pruebas. |
| **Qué mejoraríamos** | Incorporar descuentos, promociones y puntos de fidelización, manteniendo la coordinación de las operaciones de venta centralizada en la fachada. |
