## Ficha de Patrones

* **Patrón y tipo:** Singleton – Creacional

* **Problema que resuelve en NUESTRO proyecto:** Abrir una conexión nueva a la base de datos SQLite (`pos_veterinaria.db`) en cada pantalla, consulta o transacción del POS es lento, desordenado y puede generar bloqueos o múltiples accesos concurrentes innecesarios.

* **Dónde está en el código:** Se encuentra ubicado en la clase de gestión y conexión de la base de datos (`Database`), encargada de proveer el enlace único con SQLite.

* **Cómo funciona:** La clase restringe la creación de nuevos objetos haciendo su constructor privado y gestiona un atributo interno. Expone un método único (`get_instancia()`) que crea la conexión una sola vez la primera vez que se solicita y devuelve siempre esa misma instancia compartida.

* **Antes y después:** 
  * **Antes:** Se instanciaban múltiples conexiones a la base de datos de forma dispersa a lo largo del código, afectando el rendimiento.
  * **Después:** Existe una única instancia de conexión centralizada y compartida de forma segura entre todas las clases y operaciones del POS.

* **Diagrama de clases (simple):**
  [Database] (contiene constructor privado `__init__`, atributo estático `_instancia` y método estático `get_instancia()`, retornando siempre la misma referencia de conexión SQLite).

* **Cómo lo probamos:** Se realizaron pruebas solicitando múltiples veces la conexión desde diferentes puntos del código y verificando mediante aserciones que se trataba exactamente del mismo objeto en memoria (`¿misma instancia? -> True`).

* **Qué mejoraríamos:** Implementar un cierre seguro y centralizado de la conexión al finalizar la ejecución general del programa.
