import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ==========================================================
# ==========================================================
# >>>>>>>>>>>>>>>>>> E3 - PATRÓN CREACIONAL <<<<<<<<<<<<<<<<
# >>>>>>>>>>>>>>>>>> SINGLETON <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==========================================================
# ==========================================================
#
# ¿QUÉ HACE ESTE PATRÓN?
#
# Singleton permite que solamente exista una instancia de
# esta clase durante la ejecución del programa.
#
# En nuestro proyecto lo utilizamos para la conexión
# con la base de datos.
#
# Esto evita crear diferentes conexiones a la base de datos
# desde diferentes partes del programa.
#
# ESTA ES UNA DE LAS DOS PARTES IMPORTANTES DEL E3.
#
# Tipo de patrón: CREACIONAL
# Patrón: SINGLETON
# Clase: Database
#
# ==========================================================


class Database:

    # Esta variable guarda la única instancia de Database.
    _instance = None

    def __new__(cls):

        # Verificamos si todavía no existe una instancia.
        if cls._instance is None:

            # Creamos la única instancia.
            cls._instance = super(Database, cls).__new__(cls)

            # Creamos la conexión con SQLite.
            cls._instance.connection = sqlite3.connect(
                "pos_veterinaria.db"
            )

            # Permite acceder a las columnas por nombre.
            cls._instance.connection.row_factory = sqlite3.Row

            # Creamos las tablas.
            cls._instance.crear_tablas()

        # Siempre devolvemos la misma instancia.
        return cls._instance

    # ------------------------------------------------------
    # CREAR TABLAS
    # ------------------------------------------------------

    def crear_tablas(self):

        cursor = self.connection.cursor()

        # Tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                rol TEXT NOT NULL
            )
        """)

        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo TEXT UNIQUE NOT NULL,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL,
                stock INTEGER NOT NULL,
                stock_minimo INTEGER NOT NULL
            )
        """)

        # Tabla de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                usuario TEXT NOT NULL,
                medio_pago TEXT NOT NULL,
                total REAL NOT NULL
            )
        """)

        # Detalle de las ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS detalle_ventas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                venta_id INTEGER NOT NULL,
                producto_id INTEGER NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                subtotal REAL NOT NULL
            )
        """)

        # --------------------------------------------------
        # Usuario administrador inicial
        # --------------------------------------------------

        cursor.execute("""
            SELECT * FROM usuarios
            WHERE usuario = 'admin'
        """)

        usuario = cursor.fetchone()

        if usuario is None:

            cursor.execute("""
                INSERT INTO usuarios
                (nombre, usuario, password, rol)
                VALUES (?, ?, ?, ?)
            """, (
                "Administrador",
                "admin",
                "admin123",
                "Administrador"
            ))

        self.connection.commit()

    # ------------------------------------------------------
    # EJECUTAR CONSULTAS QUE MODIFICAN DATOS
    # ------------------------------------------------------

    def ejecutar(self, consulta, parametros=()):

        cursor = self.connection.cursor()

        cursor.execute(
            consulta,
            parametros
        )

        self.connection.commit()

        return cursor

    # ------------------------------------------------------
    # EJECUTAR CONSULTAS DE LECTURA
    # ------------------------------------------------------

    def consultar(self, consulta, parametros=()):

        cursor = self.connection.cursor()

        cursor.execute(
            consulta,
            parametros
        )

        return cursor.fetchall()


# ==========================================================
# ==========================================================
# >>>>>>>>>>>>>>>>>> E3 - PATRÓN ESTRUCTURAL <<<<<<<<<<<<<<
# >>>>>>>>>>>>>>>>>> FACADE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# ==========================================================
# ==========================================================
#
# ¿QUÉ HACE ESTE PATRÓN?
#
# Facade proporciona una interfaz sencilla para realizar
# una operación que internamente necesita varias acciones.
#
# En nuestro proyecto registrar una venta necesita:
#
# 1. Registrar la venta.
# 2. Consultar el stock.
# 3. Verificar que exista suficiente stock.
# 4. Descontar el inventario.
# 5. Guardar el detalle de la venta.
#
# Antes todas esas operaciones estaban directamente
# dentro de SistemaPOS.registrar_venta().
#
# Ahora las agrupamos aquí.
#
# Así SistemaPOS solamente dice:
#
#     self.venta_facade.registrar_venta(...)
#
# y la clase Facade se encarga del resto.
#
# Tipo de patrón: ESTRUCTURAL
# Patrón: FACADE
# Clase: VentaFacade
#
# ESTA ES LA SEGUNDA PARTE IMPORTANTE DEL E3.
#
# ==========================================================


class VentaFacade:

    def __init__(self, database):

        # Recibimos la conexión única creada por Singleton.
        self.db = database

    def registrar_venta(
        self,
        usuario,
        medio_pago,
        carrito
    ):

        # --------------------------------------------------
        # Calculamos el total de la venta.
        # --------------------------------------------------

        total = sum(
            item["subtotal"]
            for item in carrito
        )

        # Utilizamos la conexión de Database.
        connection = self.db.connection

        cursor = connection.cursor()

        try:

            # --------------------------------------------------
            # PASO 1:
            # Registrar la venta principal.
            # --------------------------------------------------

            cursor.execute("""
                INSERT INTO ventas
                (fecha, usuario, medio_pago, total)
                VALUES (?, ?, ?, ?)
            """, (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                usuario,
                medio_pago,
                total
            ))

            # Obtenemos el ID de la venta recién creada.
            venta_id = cursor.lastrowid

            # --------------------------------------------------
            # PASO 2:
            # Recorrer los productos del carrito.
            # --------------------------------------------------

            for item in carrito:

                # Consultamos el stock actual.
                cursor.execute("""
                    SELECT stock
                    FROM productos
                    WHERE id = ?
                """, (
                    item["producto_id"],
                ))

                producto = cursor.fetchone()

                # Verificamos que el producto exista.
                if producto is None:

                    raise Exception(
                        "Producto no encontrado."
                    )

                stock_actual = producto["stock"]

                # --------------------------------------------------
                # PASO 3:
                # Verificar stock suficiente.
                # --------------------------------------------------

                if item["cantidad"] > stock_actual:

                    raise Exception(
                        f"Stock insuficiente para "
                        f"{item['nombre']}."
                    )

                # --------------------------------------------------
                # PASO 4:
                # Calcular nuevo stock.
                # --------------------------------------------------

                nuevo_stock = (
                    stock_actual -
                    item["cantidad"]
                )

                # --------------------------------------------------
                # PASO 5:
                # Actualizar inventario.
                # --------------------------------------------------

                cursor.execute("""
                    UPDATE productos
                    SET stock = ?
                    WHERE id = ?
                """, (
                    nuevo_stock,
                    item["producto_id"]
                ))

                # --------------------------------------------------
                # PASO 6:
                # Guardar el detalle de la venta.
                # --------------------------------------------------

                cursor.execute("""
                    INSERT INTO detalle_ventas
                    (
                        venta_id,
                        producto_id,
                        cantidad,
                        precio,
                        subtotal
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    venta_id,
                    item["producto_id"],
                    item["cantidad"],
                    item["precio"],
                    item["subtotal"]
                ))

            # --------------------------------------------------
            # Si todo salió correctamente:
            # guardamos todos los cambios.
            # --------------------------------------------------

            connection.commit()

            # Devolvemos el ID de la venta.
            return venta_id, total

        except Exception:

            # Si algo falla, cancelamos los cambios.
            connection.rollback()

            # Enviamos nuevamente el error.
            raise


# ==========================================================
# ==========================================================
# APLICACIÓN PRINCIPAL
# ==========================================================
# ==========================================================


class SistemaPOS:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Sistema de Inventario y Ventas - POS"
        )

        self.root.geometry(
            "1150x700"
        )

        self.root.resizable(
            False,
            False
        )

        # --------------------------------------------------
        # SINGLETON
        # --------------------------------------------------
        #
        # Cada vez que pedimos Database(), obtenemos la
        # misma instancia.
        #
        # Esto demuestra el uso del patrón Singleton.
        # --------------------------------------------------

        self.db = Database()

        # --------------------------------------------------
        # FACADE
        # --------------------------------------------------
        #
        # Creamos la fachada para manejar el proceso
        # completo de registrar ventas.
        # --------------------------------------------------

        self.venta_facade = VentaFacade(
            self.db
        )

        self.usuario_actual = None

        self.rol_actual = None

        self.carrito = []

        self.mostrar_login()

    # ======================================================
    # LOGIN
    # ======================================================

    def limpiar_ventana(self):

        for widget in self.root.winfo_children():

            widget.destroy()

    def mostrar_login(self):

        self.limpiar_ventana()

        frame = tk.Frame(
            self.root,
            bg="#eeeeee",
            padx=40,
            pady=40
        )

        frame.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        titulo = tk.Label(
            frame,
            text="SISTEMA DE INVENTARIO Y VENTAS",
            font=("Arial", 20, "bold"),
            bg="#eeeeee"
        )

        titulo.pack(
            pady=10
        )

        subtitulo = tk.Label(
            frame,
            text="Punto de Venta - PYME",
            font=("Arial", 12),
            bg="#eeeeee"
        )

        subtitulo.pack(
            pady=5
        )

        tk.Label(
            frame,
            text="Usuario:",
            font=("Arial", 11),
            bg="#eeeeee"
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        self.txt_usuario = tk.Entry(
            frame,
            width=30,
            font=("Arial", 11)
        )

        self.txt_usuario.pack()

        tk.Label(
            frame,
            text="Contraseña:",
            font=("Arial", 11),
            bg="#eeeeee"
        ).pack(
            anchor="w",
            pady=(15, 5)
        )

        self.txt_password = tk.Entry(
            frame,
            width=30,
            show="*",
            font=("Arial", 11)
        )

        self.txt_password.pack()

        btn = tk.Button(
            frame,
            text="INICIAR SESIÓN",
            width=25,
            bg="#333333",
            fg="white",
            font=("Arial", 11, "bold"),
            command=self.iniciar_sesion
        )

        btn.pack(
            pady=25
        )

        tk.Label(
            frame,
            text="Usuario inicial: admin\nContraseña: admin123",
            font=("Arial", 9),
            bg="#eeeeee"
        ).pack()

    def iniciar_sesion(self):

        usuario = self.txt_usuario.get().strip()

        password = self.txt_password.get().strip()

        resultado = self.db.consultar("""
            SELECT * FROM usuarios
            WHERE usuario = ?
            AND password = ?
        """, (
            usuario,
            password
        ))

        if resultado:

            self.usuario_actual = (
                resultado[0]["usuario"]
            )

            self.rol_actual = (
                resultado[0]["rol"]
            )

            self.mostrar_principal()

        else:

            messagebox.showerror(
                "Error",
                "Usuario o contraseña incorrectos."
            )

    # ======================================================
    # VENTANA PRINCIPAL
    # ======================================================

    def mostrar_principal(self):

        self.limpiar_ventana()

        # --------------------------------------------------
        # ENCABEZADO
        # --------------------------------------------------

        encabezado = tk.Frame(
            self.root,
            bg="#222222",
            height=70
        )

        encabezado.pack(
            fill="x"
        )

        tk.Label(
            encabezado,
            text="SISTEMA DE INVENTARIO Y VENTAS",
            bg="#222222",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(
            side="left",
            padx=20,
            pady=18
        )

        tk.Label(
            encabezado,
            text=f"Usuario: {self.usuario_actual}",
            bg="#222222",
            fg="white",
            font=("Arial", 10)
        ).pack(
            side="right",
            padx=20
        )

        # --------------------------------------------------
        # NOTEBOOK
        # --------------------------------------------------

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tab_productos = tk.Frame(
            self.notebook
        )

        self.tab_ventas = tk.Frame(
            self.notebook
        )

        self.tab_inventario = tk.Frame(
            self.notebook
        )

        self.tab_reportes = tk.Frame(
            self.notebook
        )

        self.notebook.add(
            self.tab_productos,
            text="Productos"
        )

        self.notebook.add(
            self.tab_ventas,
            text="Registrar Venta"
        )

        self.notebook.add(
            self.tab_inventario,
            text="Inventario"
        )

        self.notebook.add(
            self.tab_reportes,
            text="Reportes"
        )

        # Crear contenido

        self.crear_tab_productos()

        self.crear_tab_ventas()

        self.crear_tab_inventario()

        self.crear_tab_reportes()

        # --------------------------------------------------
        # BOTÓN SALIR
        # --------------------------------------------------

        frame_inferior = tk.Frame(
            self.root
        )

        frame_inferior.pack(
            fill="x",
            padx=10,
            pady=5
        )

        tk.Button(
            frame_inferior,
            text="Cerrar sesión",
            command=self.mostrar_login
        ).pack(
            side="right"
        )

    # ======================================================
    # PRODUCTOS
    # ======================================================

    def crear_tab_productos(self):

        titulo = tk.Label(
            self.tab_productos,
            text="ADMINISTRACIÓN DE PRODUCTOS",
            font=("Arial", 16, "bold")
        )

        titulo.pack(
            pady=10
        )

        # --------------------------------------------------
        # FORMULARIO
        # --------------------------------------------------

        formulario = tk.LabelFrame(
            self.tab_productos,
            text="Datos del producto",
            padx=15,
            pady=15
        )

        formulario.pack(
            fill="x",
            padx=20,
            pady=5
        )

        # Código

        tk.Label(
            formulario,
            text="Código:"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.txt_codigo = tk.Entry(
            formulario,
            width=20
        )

        self.txt_codigo.grid(
            row=0,
            column=1,
            padx=5
        )

        # Nombre

        tk.Label(
            formulario,
            text="Nombre:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.txt_nombre = tk.Entry(
            formulario,
            width=20
        )

        self.txt_nombre.grid(
            row=0,
            column=3,
            padx=5
        )

        # Categoría

        tk.Label(
            formulario,
            text="Categoría:"
        ).grid(
            row=0,
            column=4,
            padx=5
        )

        self.txt_categoria = tk.Entry(
            formulario,
            width=20
        )

        self.txt_categoria.grid(
            row=0,
            column=5,
            padx=5
        )

        # Precio

        tk.Label(
            formulario,
            text="Precio:"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.txt_precio = tk.Entry(
            formulario,
            width=20
        )

        self.txt_precio.grid(
            row=1,
            column=1,
            padx=5
        )

        # Stock

        tk.Label(
            formulario,
            text="Stock:"
        ).grid(
            row=1,
            column=2,
            padx=5
        )

        self.txt_stock = tk.Entry(
            formulario,
            width=20
        )

        self.txt_stock.grid(
            row=1,
            column=3,
            padx=5
        )

        # Stock mínimo

        tk.Label(
            formulario,
            text="Stock mínimo:"
        ).grid(
            row=1,
            column=4,
            padx=5
        )

        self.txt_stock_minimo = tk.Entry(
            formulario,
            width=20
        )

        self.txt_stock_minimo.grid(
            row=1,
            column=5,
            padx=5
        )

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        botones = tk.Frame(
            self.tab_productos
        )

        botones.pack(
            pady=10
        )

        tk.Button(
            botones,
            text="Nuevo",
            width=15,
            command=self.nuevo_producto
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        tk.Button(
            botones,
            text="Guardar",
            width=15,
            command=self.guardar_producto
        ).grid(
            row=0,
            column=1,
            padx=5
        )

        tk.Button(
            botones,
            text="Editar",
            width=15,
            command=self.editar_producto
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        tk.Button(
            botones,
            text="Eliminar",
            width=15,
            command=self.eliminar_producto
        ).grid(
            row=0,
            column=3,
            padx=5
        )

        # --------------------------------------------------
        # BÚSQUEDA
        # --------------------------------------------------

        buscar_frame = tk.Frame(
            self.tab_productos
        )

        buscar_frame.pack(
            fill="x",
            padx=20,
            pady=5
        )

        tk.Label(
            buscar_frame,
            text="Buscar:"
        ).pack(
            side="left"
        )

        self.txt_buscar = tk.Entry(
            buscar_frame,
            width=30
        )

        self.txt_buscar.pack(
            side="left",
            padx=10
        )

        tk.Button(
            buscar_frame,
            text="Buscar",
            command=self.buscar_producto
        ).pack(
            side="left"
        )

        tk.Button(
            buscar_frame,
            text="Mostrar todos",
            command=self.cargar_productos
        ).pack(
            side="left",
            padx=5
        )

        # --------------------------------------------------
        # TABLA
        # --------------------------------------------------

        columnas = (
            "id",
            "codigo",
            "nombre",
            "categoria",
            "precio",
            "stock",
            "stock_minimo"
        )

        self.tabla_productos = ttk.Treeview(
            self.tab_productos,
            columns=columnas,
            show="headings",
            height=12
        )

        encabezados = {

            "id": "ID",

            "codigo": "Código",

            "nombre": "Nombre",

            "categoria": "Categoría",

            "precio": "Precio",

            "stock": "Stock",

            "stock_minimo": "Stock mínimo"
        }

        for columna in columnas:

            self.tabla_productos.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla_productos.column(
                columna,
                width=120
            )

        self.tabla_productos.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.tabla_productos.bind(
            "<ButtonRelease-1>",
            self.seleccionar_producto
        )

        self.cargar_productos()

    # ======================================================
    # PRODUCTOS - FUNCIONES
    # ======================================================

    def nuevo_producto(self):

        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_categoria.delete(
            0,
            tk.END
        )

        self.txt_precio.delete(
            0,
            tk.END
        )

        self.txt_stock.delete(
            0,
            tk.END
        )

        self.txt_stock_minimo.delete(
            0,
            tk.END
        )

        self.txt_codigo.focus()

    # ------------------------------------------------------
    # GUARDAR PRODUCTO
    # ------------------------------------------------------

    def guardar_producto(self):

        codigo = self.txt_codigo.get().strip()

        nombre = self.txt_nombre.get().strip()

        categoria = self.txt_categoria.get().strip()

        precio = self.txt_precio.get().strip()

        stock = self.txt_stock.get().strip()

        stock_minimo = self.txt_stock_minimo.get().strip()

        if not codigo or not nombre or not categoria:

            messagebox.showwarning(
                "Datos incompletos",
                "Complete los datos del producto."
            )

            return

        try:

            precio = float(precio)

            stock = int(stock)

            stock_minimo = int(stock_minimo)

            if (
                precio < 0
                or stock < 0
                or stock_minimo < 0
            ):

                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Precio y cantidades deben ser valores válidos."
            )

            return

        try:

            self.db.ejecutar("""
                INSERT INTO productos
                (
                    codigo,
                    nombre,
                    categoria,
                    precio,
                    stock,
                    stock_minimo
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                codigo,
                nombre,
                categoria,
                precio,
                stock,
                stock_minimo
            ))

            messagebox.showinfo(
                "Producto",
                "Producto registrado correctamente."
            )

            self.cargar_productos()

            self.nuevo_producto()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "El código del producto ya existe."
            )

    # ------------------------------------------------------
    # SELECCIONAR PRODUCTO
    # ------------------------------------------------------

    def seleccionar_producto(self, event):

        seleccionado = (
            self.tabla_productos.selection()
        )

        if not seleccionado:

            return

        datos = self.tabla_productos.item(
            seleccionado[0]
        )["values"]

        self.txt_codigo.delete(
            0,
            tk.END
        )

        self.txt_codigo.insert(
            0,
            datos[1]
        )

        self.txt_nombre.delete(
            0,
            tk.END
        )

        self.txt_nombre.insert(
            0,
            datos[2]
        )

        self.txt_categoria.delete(
            0,
            tk.END
        )

        self.txt_categoria.insert(
            0,
            datos[3]
        )

        self.txt_precio.delete(
            0,
            tk.END
        )

        # --------------------------------------------------
        # CORRECCIÓN DEL PRECIO PARA EDITAR
        # --------------------------------------------------
        #
        # En la tabla mostramos el precio como:
        #
        # $10,000
        #
        # pero para editar necesitamos:
        #
        # 10000
        #
        # Por eso eliminamos "$" y ",".
        # --------------------------------------------------

        precio_tabla = str(
            datos[4]
        )

        precio_limpio = (
            precio_tabla
            .replace("$", "")
            .replace(",", "")
        )

        self.txt_precio.insert(
            0,
            precio_limpio
        )

        self.txt_stock.delete(
            0,
            tk.END
        )

        self.txt_stock.insert(
            0,
            datos[5]
        )

        self.txt_stock_minimo.delete(
            0,
            tk.END
        )

        self.txt_stock_minimo.insert(
            0,
            datos[6]
        )

    # ------------------------------------------------------
    # EDITAR PRODUCTO
    # ------------------------------------------------------

    def editar_producto(self):

        seleccionado = (
            self.tabla_productos.selection()
        )

        if not seleccionado:

            messagebox.showwarning(
                "Editar",
                "Seleccione un producto."
            )

            return

        datos = self.tabla_productos.item(
            seleccionado[0]
        )["values"]

        producto_id = datos[0]

        # --------------------------------------------------
        # Obtenemos los datos directamente de los campos.
        # --------------------------------------------------

        codigo = self.txt_codigo.get().strip()

        nombre = self.txt_nombre.get().strip()

        categoria = self.txt_categoria.get().strip()

        precio_texto = self.txt_precio.get().strip()

        stock_texto = self.txt_stock.get().strip()

        stock_minimo_texto = (
            self.txt_stock_minimo.get().strip()
        )

        # Verificamos datos básicos.

        if not codigo or not nombre or not categoria:

            messagebox.showwarning(
                "Editar",
                "Complete los datos del producto."
            )

            return

        try:

            precio = float(
                precio_texto
                .replace("$", "")
                .replace(",", "")
            )

            stock = int(
                stock_texto
            )

            stock_minimo = int(
                stock_minimo_texto
            )

            if (
                precio < 0
                or stock < 0
                or stock_minimo < 0
            ):

                raise ValueError

        except:

            messagebox.showerror(
                "Error",
                "Precio y cantidades no son válidos."
            )

            return

        # --------------------------------------------------
        # ACTUALIZAR EN LA BASE DE DATOS
        # --------------------------------------------------

        try:

            self.db.ejecutar("""
                UPDATE productos

                SET codigo = ?,
                    nombre = ?,
                    categoria = ?,
                    precio = ?,
                    stock = ?,
                    stock_minimo = ?

                WHERE id = ?
            """, (
                codigo,
                nombre,
                categoria,
                precio,
                stock,
                stock_minimo,
                producto_id
            ))

            messagebox.showinfo(
                "Producto",
                "Producto actualizado correctamente."
            )

            # Actualizamos la tabla.
            self.cargar_productos()

            # Actualizamos también el inventario.
            self.cargar_inventario()

            # Actualizamos productos disponibles para ventas.
            self.cargar_combo_productos()

            # Limpiamos formulario.
            self.nuevo_producto()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Error",
                "El código del producto ya existe."
            )

    # ------------------------------------------------------
    # ELIMINAR PRODUCTO
    # ------------------------------------------------------

    def eliminar_producto(self):

        seleccionado = (
            self.tabla_productos.selection()
        )

        if not seleccionado:

            messagebox.showwarning(
                "Eliminar",
                "Seleccione un producto."
            )

            return

        datos = self.tabla_productos.item(
            seleccionado[0]
        )["values"]

        confirmar = messagebox.askyesno(
            "Eliminar",
            "¿Desea eliminar este producto?"
        )

        if confirmar:

            self.db.ejecutar("""
                DELETE FROM productos
                WHERE id = ?
            """, (
                datos[0],
            ))

            self.cargar_productos()

            self.cargar_inventario()

            self.cargar_combo_productos()

            self.nuevo_producto()

            messagebox.showinfo(
                "Producto",
                "Producto eliminado."
            )

    # ------------------------------------------------------
    # CARGAR PRODUCTOS
    # ------------------------------------------------------

    def cargar_productos(self):

        for item in (
            self.tabla_productos.get_children()
        ):

            self.tabla_productos.delete(
                item
            )

        productos = self.db.consultar("""
            SELECT *
            FROM productos
            ORDER BY id DESC
        """)

        for producto in productos:

            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto["id"],
                    producto["codigo"],
                    producto["nombre"],
                    producto["categoria"],

                    # El precio se muestra formateado.
                    f"${producto['precio']:,.0f}",

                    producto["stock"],

                    producto["stock_minimo"]
                )
            )

        if hasattr(
            self,
            "combo_producto"
        ):

            self.cargar_combo_productos()

    # ------------------------------------------------------
    # BUSCAR PRODUCTO
    # ------------------------------------------------------

    def buscar_producto(self):

        texto = (
            self.txt_buscar
            .get()
            .strip()
        )

        for item in (
            self.tabla_productos.get_children()
        ):

            self.tabla_productos.delete(
                item
            )

        productos = self.db.consultar("""
            SELECT *
            FROM productos

            WHERE codigo LIKE ?
               OR nombre LIKE ?
               OR categoria LIKE ?

            ORDER BY nombre
        """, (
            f"%{texto}%",
            f"%{texto}%",
            f"%{texto}%"
        ))

        for producto in productos:

            self.tabla_productos.insert(
                "",
                tk.END,
                values=(
                    producto["id"],
                    producto["codigo"],
                    producto["nombre"],
                    producto["categoria"],
                    f"${producto['precio']:,.0f}",
                    producto["stock"],
                    producto["stock_minimo"]
                )
            )

    # ======================================================
    # VENTAS
    # ======================================================

    def crear_tab_ventas(self):

        titulo = tk.Label(
            self.tab_ventas,
            text="REGISTRAR VENTA",
            font=("Arial", 16, "bold")
        )

        titulo.pack(
            pady=10
        )

        formulario = tk.LabelFrame(
            self.tab_ventas,
            text="Agregar producto a la venta",
            padx=15,
            pady=15
        )

        formulario.pack(
            fill="x",
            padx=20
        )

        tk.Label(
            formulario,
            text="Producto:"
        ).grid(
            row=0,
            column=0,
            padx=5
        )

        self.combo_producto = ttk.Combobox(
            formulario,
            width=40,
            state="readonly"
        )

        self.combo_producto.grid(
            row=0,
            column=1,
            padx=5
        )

        self.combo_producto.bind(
            "<<ComboboxSelected>>",
            self.actualizar_precio_producto
        )

        tk.Label(
            formulario,
            text="Cantidad:"
        ).grid(
            row=0,
            column=2,
            padx=5
        )

        self.txt_cantidad = tk.Entry(
            formulario,
            width=10
        )

        self.txt_cantidad.grid(
            row=0,
            column=3,
            padx=5
        )

        self.lbl_precio = tk.Label(
            formulario,
            text="Precio: $0"
        )

        self.lbl_precio.grid(
            row=1,
            column=1,
            sticky="w",
            pady=10
        )

        tk.Button(
            formulario,
            text="Agregar al carrito",
            command=self.agregar_carrito
        ).grid(
            row=0,
            column=4,
            padx=10
        )

        # --------------------------------------------------
        # CARRITO
        # --------------------------------------------------

        tk.Label(
            self.tab_ventas,
            text="Productos de la venta",
            font=("Arial", 12, "bold")
        ).pack(
            pady=10
        )

        columnas = (
            "producto",
            "cantidad",
            "precio",
            "subtotal"
        )

        self.tabla_carrito = ttk.Treeview(
            self.tab_ventas,
            columns=columnas,
            show="headings",
            height=10
        )

        encabezados = {

            "producto": "Producto",

            "cantidad": "Cantidad",

            "precio": "Precio",

            "subtotal": "Subtotal"
        }

        for columna in columnas:

            self.tabla_carrito.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla_carrito.column(
                columna,
                width=180
            )

        self.tabla_carrito.pack(
            padx=20,
            pady=5
        )

        # --------------------------------------------------
        # QUITAR PRODUCTO
        # --------------------------------------------------

        tk.Button(
            self.tab_ventas,
            text="Quitar producto",
            command=self.quitar_carrito
        ).pack(
            pady=5
        )

        # --------------------------------------------------
        # TOTAL
        # --------------------------------------------------

        self.lbl_total = tk.Label(
            self.tab_ventas,
            text="TOTAL: $0",
            font=("Arial", 18, "bold")
        )

        self.lbl_total.pack(
            pady=10
        )

        # --------------------------------------------------
        # MEDIO DE PAGO
        # --------------------------------------------------

        pago_frame = tk.Frame(
            self.tab_ventas
        )

        pago_frame.pack(
            pady=5
        )

        tk.Label(
            pago_frame,
            text="Medio de pago:"
        ).pack(
            side="left"
        )

        self.combo_pago = ttk.Combobox(
            pago_frame,
            values=[
                "Efectivo",
                "Tarjeta",
                "Transferencia"
            ],
            state="readonly",
            width=20
        )

        self.combo_pago.current(
            0
        )

        self.combo_pago.pack(
            side="left",
            padx=10
        )

        # --------------------------------------------------
        # CONFIRMAR VENTA
        # --------------------------------------------------

        tk.Button(
            self.tab_ventas,
            text="REGISTRAR VENTA",
            width=25,
            height=2,
            font=("Arial", 11, "bold"),
            command=self.registrar_venta
        ).pack(
            pady=10
        )

        self.cargar_combo_productos()

    # ======================================================
    # VENTAS - FUNCIONES
    # ======================================================

    def cargar_combo_productos(self):

        productos = self.db.consultar("""
            SELECT *
            FROM productos
            ORDER BY nombre
        """)

        self.productos_combo = productos

        valores = []

        for producto in productos:

            valores.append(
                f"{producto['codigo']} - "
                f"{producto['nombre']}"
            )

        self.combo_producto["values"] = valores

    # ------------------------------------------------------
    # ACTUALIZAR PRECIO
    # ------------------------------------------------------

    def actualizar_precio_producto(
        self,
        event=None
    ):

        indice = (
            self.combo_producto.current()
        )

        if indice < 0:

            return

        producto = (
            self.productos_combo[indice]
        )

        self.lbl_precio.config(
            text=(
                f"Precio: "
                f"${producto['precio']:,.0f}"
            )
        )

    # ------------------------------------------------------
    # AGREGAR AL CARRITO
    # ------------------------------------------------------

    def agregar_carrito(self):

        indice = (
            self.combo_producto.current()
        )

        if indice < 0:

            messagebox.showwarning(
                "Venta",
                "Seleccione un producto."
            )

            return

        try:

            cantidad = int(
                self.txt_cantidad.get()
            )

            if cantidad <= 0:

                raise ValueError

        except:

            messagebox.showerror(
                "Cantidad",
                "Ingrese una cantidad válida."
            )

            return

        producto = (
            self.productos_combo[indice]
        )

        if cantidad > producto["stock"]:

            messagebox.showerror(
                "Stock insuficiente",
                f"Stock disponible: "
                f"{producto['stock']}"
            )

            return

        # --------------------------------------------------
        # Revisar si ya está en el carrito.
        # --------------------------------------------------

        for item in self.carrito:

            if (
                item["producto_id"]
                ==
                producto["id"]
            ):

                nueva_cantidad = (
                    item["cantidad"]
                    +
                    cantidad
                )

                if (
                    nueva_cantidad
                    >
                    producto["stock"]
                ):

                    messagebox.showerror(
                        "Stock insuficiente",
                        "La cantidad supera "
                        "el stock disponible."
                    )

                    return

                item["cantidad"] = (
                    nueva_cantidad
                )

                item["subtotal"] = (
                    nueva_cantidad
                    *
                    producto["precio"]
                )

                self.actualizar_carrito()

                return

        # --------------------------------------------------
        # Crear nuevo elemento del carrito.
        # --------------------------------------------------

        item = {

            "producto_id":
                producto["id"],

            "nombre":
                producto["nombre"],

            "precio":
                producto["precio"],

            "cantidad":
                cantidad,

            "subtotal":
                cantidad
                *
                producto["precio"]
        }

        self.carrito.append(
            item
        )

        self.actualizar_carrito()

        self.txt_cantidad.delete(
            0,
            tk.END
        )

    # ------------------------------------------------------
    # ACTUALIZAR CARRITO
    # ------------------------------------------------------

    def actualizar_carrito(self):

        for item in (
            self.tabla_carrito.get_children()
        ):

            self.tabla_carrito.delete(
                item
            )

        total = 0

        for item in self.carrito:

            self.tabla_carrito.insert(
                "",
                tk.END,
                values=(
                    item["nombre"],
                    item["cantidad"],
                    f"${item['precio']:,.0f}",
                    f"${item['subtotal']:,.0f}"
                )
            )

            total += item["subtotal"]

        self.lbl_total.config(
            text=f"TOTAL: ${total:,.0f}"
        )

    # ------------------------------------------------------
    # QUITAR DEL CARRITO
    # ------------------------------------------------------

    def quitar_carrito(self):

        seleccionado = (
            self.tabla_carrito.selection()
        )

        if not seleccionado:

            messagebox.showwarning(
                "Carrito",
                "Seleccione un producto."
            )

            return

        indice = (
            self.tabla_carrito.index(
                seleccionado[0]
            )
        )

        self.carrito.pop(
            indice
        )

        self.actualizar_carrito()

    # ======================================================
    # ======================================================
    # >>>>>>>>>>>>>>>>>> E3 - FACADE EN ACCIÓN <<<<<<<<<<<<
    # >>>>>>>>>>>>>>>>>> REGISTRAR VENTA <<<<<<<<<<<<<<<<<<<
    # ======================================================
    # ======================================================
    #
    # IMPORTANTE:
    #
    # Esta función ya NO contiene toda la lógica de la venta.
    #
    # Ahora solamente:
    #
    # 1. Verifica que exista carrito.
    # 2. Obtiene medio de pago.
    # 3. Calcula el total para mostrarlo.
    # 4. Pide confirmación.
    # 5. Llama a VentaFacade.
    #
    # La clase VentaFacade se encarga de:
    #
    # - Registrar venta.
    # - Consultar stock.
    # - Verificar stock.
    # - Descontar inventario.
    # - Registrar detalle.
    #
    # Esto es justamente lo que queremos demostrar
    # con el patrón FACADE.
    #
    # ======================================================

    def registrar_venta(self):

        # --------------------------------------------------
        # Verificar que el carrito no esté vacío.
        # --------------------------------------------------

        if not self.carrito:

            messagebox.showwarning(
                "Venta",
                "El carrito está vacío."
            )

            return

        # --------------------------------------------------
        # Obtener medio de pago.
        # --------------------------------------------------

        medio_pago = (
            self.combo_pago.get()
        )

        # --------------------------------------------------
        # Calcular total.
        #
        # Esto solamente se utiliza para mostrar la
        # confirmación al usuario.
        # --------------------------------------------------

        total = sum(
            item["subtotal"]
            for item in self.carrito
        )

        # --------------------------------------------------
        # Confirmar venta.
        # --------------------------------------------------

        confirmar = messagebox.askyesno(
            "Confirmar venta",

            f"Total de la venta: "
            f"${total:,.0f}\n\n"
            "¿Desea registrar la venta?"
        )

        if not confirmar:

            return

        try:

            # ==================================================
            # AQUÍ LLAMAMOS AL PATRÓN FACADE
            # ==================================================
            #
            # Una sola llamada ejecuta internamente:
            #
            # registrar venta
            #       ↓
            # verificar stock
            #       ↓
            # descontar inventario
            #       ↓
            # guardar detalle
            #
            # ==================================================

            venta_id, total = (
                self.venta_facade.registrar_venta(
                    self.usuario_actual,
                    medio_pago,
                    self.carrito
                )
            )

            # --------------------------------------------------
            # Mostrar confirmación.
            # --------------------------------------------------

            messagebox.showinfo(
                "Venta registrada",

                "La venta se registró correctamente.\n\n"
                "El inventario fue actualizado automáticamente."
            )

            # --------------------------------------------------
            # Limpiar carrito.
            # --------------------------------------------------

            self.carrito = []

            self.actualizar_carrito()

            # --------------------------------------------------
            # Actualizar las diferentes partes del sistema.
            # --------------------------------------------------

            self.cargar_combo_productos()

            self.cargar_productos()

            self.cargar_inventario()

            self.cargar_reportes()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error)
            )

    # ======================================================
    # INVENTARIO
    # ======================================================

    def crear_tab_inventario(self):

        titulo = tk.Label(
            self.tab_inventario,
            text="CONSULTA DE INVENTARIO",
            font=("Arial", 16, "bold")
        )

        titulo.pack(
            pady=10
        )

        self.lbl_alertas = tk.Label(
            self.tab_inventario,
            text="",
            font=("Arial", 12, "bold")
        )

        self.lbl_alertas.pack(
            pady=5
        )

        columnas = (
            "codigo",
            "nombre",
            "categoria",
            "precio",
            "stock",
            "minimo",
            "estado"
        )

        self.tabla_inventario = ttk.Treeview(
            self.tab_inventario,
            columns=columnas,
            show="headings",
            height=18
        )

        encabezados = {

            "codigo": "Código",

            "nombre": "Producto",

            "categoria": "Categoría",

            "precio": "Precio",

            "stock": "Stock",

            "minimo": "Stock mínimo",

            "estado": "Estado"
        }

        for columna in columnas:

            self.tabla_inventario.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla_inventario.column(
                columna,
                width=140
            )

        self.tabla_inventario.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        tk.Button(
            self.tab_inventario,
            text="Actualizar inventario",
            command=self.cargar_inventario
        ).pack(
            pady=5
        )

        self.cargar_inventario()

    # ------------------------------------------------------
    # CARGAR INVENTARIO
    # ------------------------------------------------------

    def cargar_inventario(self):

        if not hasattr(
            self,
            "tabla_inventario"
        ):

            return

        for item in (
            self.tabla_inventario.get_children()
        ):

            self.tabla_inventario.delete(
                item
            )

        productos = self.db.consultar("""
            SELECT *
            FROM productos
            ORDER BY nombre
        """)

        alertas = 0

        for producto in productos:

            if (
                producto["stock"]
                <=
                producto["stock_minimo"]
            ):

                estado = "BAJO STOCK"

                alertas += 1

            else:

                estado = "Disponible"

            self.tabla_inventario.insert(
                "",
                tk.END,
                values=(
                    producto["codigo"],
                    producto["nombre"],
                    producto["categoria"],
                    f"${producto['precio']:,.0f}",
                    producto["stock"],
                    producto["stock_minimo"],
                    estado
                )
            )

        if alertas > 0:

            self.lbl_alertas.config(
                text=(
                    f"⚠ Hay {alertas} "
                    f"producto(s) con bajo stock."
                )
            )

        else:

            self.lbl_alertas.config(
                text=(
                    "Inventario sin alertas "
                    "de bajo stock."
                )
            )

    # ======================================================
    # REPORTES
    # ======================================================

    def crear_tab_reportes(self):

        titulo = tk.Label(
            self.tab_reportes,
            text="REPORTES DE VENTAS",
            font=("Arial", 16, "bold")
        )

        titulo.pack(
            pady=10
        )

        columnas = (
            "id",
            "fecha",
            "usuario",
            "medio",
            "total"
        )

        self.tabla_reportes = ttk.Treeview(
            self.tab_reportes,
            columns=columnas,
            show="headings",
            height=18
        )

        encabezados = {

            "id": "Venta",

            "fecha": "Fecha",

            "usuario": "Usuario",

            "medio": "Medio de pago",

            "total": "Total"
        }

        for columna in columnas:

            self.tabla_reportes.heading(
                columna,
                text=encabezados[columna]
            )

            self.tabla_reportes.column(
                columna,
                width=170
            )

        self.tabla_reportes.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.lbl_total_ventas = tk.Label(
            self.tab_reportes,
            text="TOTAL VENDIDO: $0",
            font=("Arial", 14, "bold")
        )

        self.lbl_total_ventas.pack(
            pady=5
        )

        tk.Button(
            self.tab_reportes,
            text="Actualizar reporte",
            command=self.cargar_reportes
        ).pack(
            pady=5
        )

        self.cargar_reportes()

    # ------------------------------------------------------
    # CARGAR REPORTES
    # ------------------------------------------------------

    def cargar_reportes(self):

        if not hasattr(
            self,
            "tabla_reportes"
        ):

            return

        for item in (
            self.tabla_reportes.get_children()
        ):

            self.tabla_reportes.delete(
                item
            )

        ventas = self.db.consultar("""
            SELECT *
            FROM ventas
            ORDER BY id DESC
        """)

        total_general = 0

        for venta in ventas:

            self.tabla_reportes.insert(
                "",
                tk.END,
                values=(
                    venta["id"],
                    venta["fecha"],
                    venta["usuario"],
                    venta["medio_pago"],
                    f"${venta['total']:,.0f}"
                )
            )

            total_general += (
                venta["total"]
            )

        self.lbl_total_ventas.config(
            text=(
                f"TOTAL VENDIDO: "
                f"${total_general:,.0f}"
            )
        )


# ==========================================================
# ==========================================================
# EJECUCIÓN DEL PROGRAMA
# ==========================================================
# ==========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = SistemaPOS(
        root
    )

    root.mainloop()