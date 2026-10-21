# Sistema de Inventario y Ventas POS (Veterinaria)

Prototipo de software desarrollado para la gestión de inventario y ventas, integrando patrones de diseño de software (Creacionales y Estructurales) como parte del Corte 2 de Ingeniería de Software II.

## Integrantes del Equipo
* Andrey Alirio Pinzón Baltazar
* Yoni Steben Torres Quintero
* Cielo Nikol Solarte Lopez

## Patrones de Diseño Implementados
* **Patrón Creacional (Singleton):** Utilizado para gestionar la conexión única a la base de datos (`pos_veterinaria.db`) y evitar aperturas múltiples innecesarias.
* **Patrón Estructural (Facade / Decorator):** Implementado para simplificar la coordinación en el flujo de registro de ventas y control de inventario.

---

## Cómo Ejecutar el Proyecto en 3 Pasos

1. **Clonar o descargar el repositorio:**
   Clona este repositorio en tu computadora o descárgalo como archivo ZIP y descomprímelo.

2. **Verificar los archivos principales:**
   Asegúrate de que en la misma carpeta se encuentren tanto `main.py` como la base de datos `pos_veterinaria.db`.

3. **Ejecutar el programa desde la terminal:**
   Abre una terminal en la carpeta del proyecto y ejecuta el siguiente comando:
   ```bash
   python main.py
