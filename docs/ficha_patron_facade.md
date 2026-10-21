## Ficha de Patrones 

* **Patrón y tipo:** Facade (Fachada) – Estructural

* **Problema que resuelve en NUESTRO proyecto:** El sistema POS requería registrar una venta coordinando múltiples operaciones complejas manualmente (validar stock, calcular totales, descontar inventario, crear el registro maestro y almacenar ítems detallados), lo que sobrecargaba la interfaz gráfica y corrompía datos si fallaba un paso.

* **Dónde está en el código:** En el archivo `main.py`, dentro de la clase `VentaFacade` y su método `registrar_venta()`, el cual es invocado directamente desde la interfaz gráfica de Tkinter.

* **Cómo funciona:** La clase `VentaFacade` actúa como una interfaz unificada que encapsula todo el flujo transaccional. La interfaz solo invoca un método enviando los datos, mientras la fachada gestiona la validación, la base de datos y el control de transacciones (`commit` / `rollback`) de forma segura.
* **Antes y después:** 
  * **Antes:** Lógica de negocio dispersa en la interfaz con múltiples consultas SQL directas y alto riesgo de inconsistencia.
  * **Después:** Una sola línea (`VentaFacade.registrar_venta(...)`) ejecuta y encapsula todo el subsistema comercial limpiamente.

* **Diagrama de clases (simple):**
  [Interfaz Gráfica - Tkinter] ➔ (usa) ➔ [VentaFacade] ➔ (coordina) ➔ [Base de Datos / SQLite] y [Inventario]

* **Cómo lo probamos:** Se probó con un flujo de venta normal con stock suficiente (descuenta y guarda exitosamente) y un caso de error controlado con stock insuficiente (ejecuta `rollback` y no altera los datos).

* **Qué mejoraríamos:** Integrar reglas dinámicas adicionales como descuentos por fidelización o selección de múltiples métodos de pago.
