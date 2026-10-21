# Ficha del patrón Facade (Fachada)

## 1. Patrón y tipo

**Nombre:** Facade (Fachada)  
**Tipo:** Estructural  
**Archivo:** `main.py`  
**Clase principal:** `VentaFacade`  
**Método principal:** `registrar_venta()`

## 2. Problema que resuelve en nuestro proyecto

En el sistema POS de la veterinaria, registrar una venta requiere coordinar varias operaciones: calcular el total, registrar la venta principal, consultar y validar el stock de los productos, actualizar el inventario y guardar el detalle de la venta.

Si toda esta lógica se encuentra dentro de la interfaz gráfica, la clase que administra las pantallas también debe conocer demasiados detalles de la lógica comercial y de la base de datos.

El patrón Facade permite agrupar estas operaciones detrás de una interfaz sencilla, facilitando la organización y el mantenimiento del código.

## 3. ¿Dónde está implementado?

La implementación se encuentra en el archivo `main.py`, dentro de la clase `VentaFacade`, específicamente en el método `registrar_venta()`.

La clase `SistemaPOS` crea la fachada mediante `VentaFacade(self.db)` y la utiliza para delegar el registro de las ventas.

La fachada utiliza la conexión SQLite recibida a través del objeto `Database` y coordina las siguientes operaciones:

1. Calcular el total de la venta.
2. Registrar la venta principal.
3. Consultar y validar la existencia y el stock de cada producto.
4. Descontar las unidades vendidas del inventario.
5. Guardar los detalles de la venta.
6. Confirmar los cambios mediante `commit()` si todo sale bien.
7. Cancelar los cambios mediante `rollback()` si ocurre una excepción.

## 4. ¿Cómo funciona?

La interfaz gráfica entrega a la fachada los datos necesarios para registrar la venta. La fachada coordina las operaciones de base de datos y el control de la transacción.

De esta manera, `SistemaPOS` no necesita ejecutar directamente cada consulta SQL relacionada con el registro completo de la venta desde el punto de entrada de esa operación.

## 5. Antes y después

**Antes de aplicar Facade:** la lógica para registrar una venta se encontraba directamente en el flujo de la interfaz, que debía coordinar diferentes operaciones relacionadas con la venta y el inventario.

**Después de aplicar Facade:** la clase `VentaFacade` concentra la lógica de registro de la venta. La interfaz delega el proceso a `registrar_venta()`, mientras la fachada coordina las operaciones y controla la transacción.

Esto facilita el mantenimiento del sistema y ayuda a evitar que una venta quede parcialmente guardada cuando ocurre un error durante la transacción.

## 6. Diagrama de clases

```text
+----------------------+
|      SistemaPOS      |
+----------------------+
| - db                 |
| - venta_facade       |
+----------------------+
          |
          | utiliza
          v
+----------------------+
|     VentaFacade      |
+----------------------+
| - db                 |
+----------------------+
| + registrar_venta()  |
+----------------------+
          |
          | utiliza
          v
+----------------------+
|       Database       |
+----------------------+
| - connection         |
+----------------------+
          |
          | conecta con
          v
+----------------------+
|     SQLite           |
| pos_veterinaria.db   |
+----------------------+
```

## 7. ¿Cómo lo probamos?

Para comprobar el funcionamiento de la fachada, se deben verificar dos escenarios:

- **Venta normal:** registrar una venta con stock suficiente y comprobar que se guarden la venta y sus detalles, y que el inventario se descuente correctamente.
- **Error controlado:** intentar registrar una venta cuyo stock sea insuficiente y comprobar que la transacción se revierta, sin guardar cambios parciales.

Las pruebas deben ejecutarse en el sistema y sus resultados deben verificarse en la interfaz o en la base de datos.

## 8. ¿Qué mejoraríamos?

Se podría ampliar la fachada para incorporar reglas de descuentos, promociones, programas de fidelización y validaciones adicionales, manteniendo el proceso de venta organizado y separado de la interfaz gráfica.
